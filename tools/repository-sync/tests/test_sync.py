import http.server
import json
import os
import shutil
import subprocess
import sys
import tempfile
import threading
import unittest
import urllib.parse
from pathlib import Path


class SyncTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.module = self.root / "tools/repository-sync"
        self.module.mkdir(parents=True)
        self.original = Path(__file__).resolve().parents[1]
        shutil.copy2(self.original / "sync.py", self.module / "sync.py")
        self.env = dict(os.environ, HOME=str(self.root), GIT_CONFIG_GLOBAL=os.devnull,
                        GIT_CONFIG_NOSYSTEM="1", GIT_TERMINAL_PROMPT="0", LC_ALL="C")
        self.records = {"courses": []}
        self.failed_org = None
        self.requests = []
        self.logs = []
        owner = self

        class API(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                parsed = urllib.parse.urlsplit(self.path)
                org = parsed.path.split("/")[-2]
                page = int(urllib.parse.parse_qs(parsed.query)["page"][0])
                owner.requests.append((org, page))
                if org == owner.failed_org:
                    status, body = 403, b'{"message":"fixture denied"}'
                else:
                    status = 200
                    body = json.dumps(owner.records[org][(page - 1) * 100:page * 100]).encode()
                owner.logs.append(f"HTTP {self.path}: {status}\n{body.decode()}\n")
                self.send_response(status)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, *args):
                pass

        self.server = http.server.HTTPServer(("127.0.0.1", 0), API)
        self.addCleanup(self.server.server_close)
        self.addCleanup(self.server.shutdown)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.api = f"http://127.0.0.1:{self.server.server_port}"
        (self.module / "sources.conf").write_text(f"materials;{self.api};courses;;;current;mirror\n")

    def tearDown(self):
        print(f"\n=== {self.id()} raw logs ===")
        for entry in self.logs:
            print(entry, end="")

    def git(self, directory, *args):
        result = subprocess.run(["git", "-C", str(directory), *args], env=self.env,
                                capture_output=True, text=True, timeout=30)
        self.logs.append(f"$ git -C {directory} {' '.join(args)}\n{result.stdout}{result.stderr}")
        if result.returncode:
            self.fail(f"fixture Git failed: {args}\n{result.stderr}")
        return result.stdout.strip()

    def remote(self, org, repo, text):
        source = self.root / "seeds" / org / repo
        remote = self.root / "remotes" / org / f"{repo}.git"
        source.mkdir(parents=True)
        remote.parent.mkdir(parents=True, exist_ok=True)
        self.git(source, "init", "-q", "-b", "main")
        self.git(source, "config", "user.email", "sync@example.invalid")
        self.git(source, "config", "user.name", "Sync Test")
        (source / "README.md").write_text(text)
        self.git(source, "add", "README.md")
        self.git(source, "commit", "-q", "-m", "initial")
        self.git(self.root, "clone", "-q", "--bare", str(source), str(remote))
        self.records.setdefault(org, []).append({"name": repo, "clone_url": remote.as_uri()})
        return source, remote

    def advance(self, source, remote, text):
        (source / "README.md").write_text(text)
        self.git(source, "add", "README.md")
        self.git(source, "commit", "-q", "-m", "advance")
        self.git(source, "push", "-q", str(remote), "HEAD")
        return self.git(source, "rev-parse", "HEAD")

    def run_sync(self, *args):
        result = subprocess.run([sys.executable, str(self.module / "sync.py"), *args],
                                cwd=self.root, env=self.env, capture_output=True, text=True, timeout=60)
        self.logs.append(f"$ sync.py {' '.join(args)} [exit {result.returncode}]\n{result.stdout}{result.stderr}")
        return result

    def test_material_updates_but_personal_branch_head_index_and_worktree_survive(self):
        material, material_remote = self.remote("courses", "DSCI_511_material_students", "material old\n")
        work, work_remote = self.remote("courses", "DSCI_511_lab1_yz2000", "work old\n")
        (self.module / "sources.conf").write_text(
            f"materials;{self.api};courses;;_yz2000$;current;mirror\n"
            f"assignments;{self.api};courses;_yz2000$;;work;work\n")
        first = self.run_sync()
        self.assertEqual(first.returncode, 0, first.stderr)
        mirror = self.root / "DSCI_511/official/current/DSCI_511_material_students"
        checkout = self.root / "DSCI_511/assignments/lab1/DSCI_511_lab1_yz2000"
        self.git(checkout, "checkout", "-q", "-b", "personal-work")
        old_head = self.git(checkout, "rev-parse", "HEAD")
        (checkout / "README.md").write_text("local edit\n")
        self.git(checkout, "add", "README.md")
        old_index = self.git(checkout, "diff", "--cached")
        (checkout / "notes.txt").write_text("personal notes\n")
        (mirror / "README.md").write_text("mirror edit\n")
        (mirror / "notes.txt").write_text("mirror notes\n")
        material_head = self.advance(material, material_remote, "material new\n")
        work_head = self.advance(work, work_remote, "work new\n")
        result = self.run_sync()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.git(mirror, "rev-parse", "HEAD"), material_head)
        self.assertEqual((mirror / "README.md").read_text(), "material new\n")
        self.assertEqual((mirror / "notes.txt").read_text(), "mirror notes\n")
        self.assertEqual(self.git(checkout, "rev-parse", "HEAD"), old_head)
        self.assertEqual(self.git(checkout, "branch", "--show-current"), "personal-work")
        self.assertEqual(self.git(checkout, "rev-parse", "origin/main"), work_head)
        self.assertEqual(self.git(checkout, "diff", "--cached"), old_index)
        self.assertEqual((checkout / "README.md").read_text(), "local edit\n")
        self.assertEqual((checkout / "notes.txt").read_text(), "personal notes\n")

    def test_unchanged_mirror_retains_tracked_and_untracked_edits(self):
        self.remote("courses", "DSCI_511_material_students", "original\n")
        first = self.run_sync()
        self.assertEqual(first.returncode, 0, first.stderr)
        target = self.root / "DSCI_511/official/current/DSCI_511_material_students"
        head = self.git(target, "rev-parse", "HEAD")
        (target / "README.md").write_text("local edit\n")
        (target / "local.txt").write_text("untracked\n")
        result = self.run_sync()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.git(target, "rev-parse", "HEAD"), head)
        self.assertEqual((target / "README.md").read_text(), "local edit\n")
        self.assertEqual((target / "local.txt").read_text(), "untracked\n")

    def test_production_source_filters_choose_cl_512_materials_and_work(self):
        self.records = {org: [] for org in ("mds-2026-27", "MDS-CL-2026-27", "UBC-MDS")}
        _, v_material = self.remote("mds-2026-27", "DSCI_512_material_students", "V material\n")
        _, cl_material = self.remote("MDS-CL-2026-27", "DSCI_512_material_students", "CL material\n")
        _, v_work = self.remote("mds-2026-27", "DSCI_512_lab1_yz2000", "V work\n")
        _, cl_work = self.remote("MDS-CL-2026-27", "DSCI_512_lab1_yz2000", "CL work\n")
        _, other_work = self.remote("mds-2026-27", "DSCI_531_lab2_yz2000", "other work\n")
        self.remote("mds-2026-27", "DSCI_511_material_students", "old material\n")
        self.remote("mds-2026-27", "DSCI_511_lab1_yz2000", "old work\n")
        old_public, old_public_remote = self.remote("UBC-MDS", "DSCI_551_history", "old public\n")
        active_public, active_public_remote = self.remote("UBC-MDS", "DSCI_531_history", "active public\n")
        old_target = self.root / "DSCI_551/official/public/DSCI_551_history"
        active_target = self.root / "DSCI_531/official/public/DSCI_531_history"
        for target, remote in ((old_target, old_public_remote), (active_target, active_public_remote)):
            target.parent.mkdir(parents=True)
            self.git(self.root, "clone", "-q", str(remote), str(target))
        old_head = self.git(old_target, "rev-parse", "HEAD")
        self.advance(old_public, old_public_remote, "old public remote changed\n")
        active_head = self.advance(active_public, active_public_remote, "active public remote changed\n")
        config = (self.original / "sources.conf").read_text()
        (self.module / "sources.conf").write_text(
            config.replace("https://github.ubc.ca/api/v3", self.api).replace("https://api.github.com", self.api))
        result = self.run_sync()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((self.root / "DSCI_512/official/current/DSCI_512_material_students/README.md").read_text(), "CL material\n")
        self.assertEqual((self.root / "DSCI_512/assignments/lab1/DSCI_512_lab1_yz2000/README.md").read_text(), "CL work\n")
        self.assertEqual((self.root / "DSCI_531/assignments/lab2/DSCI_531_lab2_yz2000/README.md").read_text(), "other work\n")
        self.assertFalse((self.root / "DSCI_511").exists())
        self.assertEqual(self.git(old_target, "rev-parse", "HEAD"), old_head)
        self.assertEqual((old_target / "README.md").read_text(), "old public\n")
        self.assertEqual(self.git(active_target, "rev-parse", "HEAD"), active_head)
        self.assertEqual((active_target / "README.md").read_text(), "active public remote changed\n")
        self.assertEqual((self.module / "public.txt").read_text().splitlines(), [active_public_remote.as_uri()])
        self.assertEqual((self.module / "current.txt").read_text().splitlines(), [cl_material.as_uri()])
        self.assertEqual(set((self.module / "work.txt").read_text().splitlines()), {cl_work.as_uri(), other_work.as_uri()})
        self.assertNotIn(v_material.as_uri(), (self.module / "current.txt").read_text())
        self.assertNotIn(v_work.as_uri(), (self.module / "work.txt").read_text())

    def test_public_updates_retained_checkout_without_recreating_discarded_history(self):
        source, remote = self.remote("courses", "DSCI_523_history", "old history\n")
        _, discarded = self.remote("courses", "DSCI_531_history", "discarded history\n")
        (self.module / "sources.conf").write_text(f"public;{self.api};courses;^(DSCI|COLX)_;;public;mirror\n")
        target = self.root / "DSCI_523/official/public/DSCI_523_history"
        target.parent.mkdir(parents=True)
        self.git(self.root, "clone", "-q", str(remote), str(target))
        new_head = self.advance(source, remote, "new history\n")
        result = self.run_sync()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.git(target, "rev-parse", "HEAD"), new_head)
        self.assertEqual((target / "README.md").read_text(), "new history\n")
        self.assertFalse((self.root / "DSCI_531/official/public/DSCI_531_history").exists())
        self.assertEqual(set((self.module / "public.txt").read_text().splitlines()), {remote.as_uri(), discarded.as_uri()})

    def test_global_conflict_blocks_an_earlier_checkout_and_manifest_publication(self):
        safe, remote = self.remote("courses", "DSCI_511_safe_students", "old safe\n")
        self.remote("courses", "DSCI_523_shared_students", "one\n")
        self.remote("other", "DSCI_523_shared_students", "two\n")
        target = self.root / "DSCI_511/official/current/DSCI_511_safe_students"
        target.parent.mkdir(parents=True)
        self.git(self.root, "clone", "-q", str(remote), str(target))
        old = self.git(target, "rev-parse", "HEAD")
        self.advance(safe, remote, "new safe\n")
        (self.module / "current.txt").write_text("old inventory\n")
        (self.module / "sources.conf").write_text(
            f"one;{self.api};courses;;;current;mirror\ntwo;{self.api};other;;;current;mirror\n")
        result = self.run_sync()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.git(target, "rev-parse", "HEAD"), old)
        self.assertEqual(self.git(target, "rev-parse", "origin/main"), old)
        self.assertEqual((self.module / "current.txt").read_text(), "old inventory\n")
        self.assertFalse((self.root / "DSCI_523/official/current/DSCI_523_shared_students").exists())

    def test_api_failure_prevents_updates_and_preserves_inventory(self):
        source, remote = self.remote("courses", "DSCI_511_safe_students", "old\n")
        target = self.root / "DSCI_511/official/current/DSCI_511_safe_students"
        target.parent.mkdir(parents=True)
        self.git(self.root, "clone", "-q", str(remote), str(target))
        old = self.git(target, "rev-parse", "HEAD")
        self.advance(source, remote, "new\n")
        self.failed_org = "denied"
        (self.module / "sources.conf").write_text(
            f"one;{self.api};courses;;;current;mirror\ntwo;{self.api};denied;;;current;mirror\n")
        (self.module / "current.txt").write_text("old inventory\n")
        result = self.run_sync()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.git(target, "rev-parse", "HEAD"), old)
        self.assertEqual(self.git(target, "rev-parse", "origin/main"), old)
        self.assertEqual((self.module / "current.txt").read_text(), "old inventory\n")

    def test_origin_mismatch_stops_before_any_target_update(self):
        safe, safe_remote = self.remote("courses", "DSCI_511_safe_students", "old safe\n")
        self.remote("courses", "DSCI_525_origin_students", "expected\n")
        _, wrong = self.remote("other", "DSCI_525_origin_students", "wrong\n")
        safe_target = self.root / "DSCI_511/official/current/DSCI_511_safe_students"
        wrong_target = self.root / "DSCI_525/official/current/DSCI_525_origin_students"
        for remote, target in ((safe_remote, safe_target), (wrong, wrong_target)):
            target.parent.mkdir(parents=True)
            self.git(self.root, "clone", "-q", str(remote), str(target))
        old = self.git(safe_target, "rev-parse", "HEAD")
        self.advance(safe, safe_remote, "new safe\n")
        (self.module / "current.txt").write_text("old inventory\n")
        result = self.run_sync()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.git(safe_target, "rev-parse", "origin/main"), old)
        self.assertEqual((wrong_target / "README.md").read_text(), "wrong\n")
        self.assertEqual((self.module / "current.txt").read_text(), "old inventory\n")

    def test_missing_origin_is_not_silently_replaced(self):
        _, remote = self.remote("courses", "DSCI_511_material_students", "old\n")
        target = self.root / "DSCI_511/official/current/DSCI_511_material_students"
        target.parent.mkdir(parents=True)
        self.git(self.root, "clone", "-q", str(remote), str(target))
        self.git(target, "remote", "remove", "origin")
        result = self.run_sync()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.git(target, "remote"), "")
        self.assertEqual((target / "README.md").read_text(), "old\n")
        self.assertFalse((self.module / "current.txt").exists())

    def test_occupied_non_git_target_is_not_overwritten(self):
        self.remote("courses", "DSCI_511_material_students", "remote\n")
        target = self.root / "DSCI_511/official/current/DSCI_511_material_students"
        target.mkdir(parents=True)
        (target / "local.txt").write_text("keep me\n")
        result = self.run_sync()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual((target / "local.txt").read_text(), "keep me\n")
        self.assertFalse((target / ".git").exists())
        self.assertFalse((self.module / "current.txt").exists())

    def test_pagination_discovers_and_clones_the_second_page(self):
        self.records["courses"] = [{"name": f"utility_{i}", "clone_url": f"https://example.invalid/courses/utility_{i}.git"} for i in range(100)]
        _, remote = self.remote("courses", "DSCI_531_late_students", "second page\n")
        result = self.run_sync()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.requests, [("courses", 1), ("courses", 2)])
        self.assertEqual((self.root / "DSCI_531/official/current/DSCI_531_late_students/README.md").read_text(), "second page\n")
        self.assertIn(remote.as_uri(), (self.module / "current.txt").read_text().splitlines())

    def test_invalid_api_entry_prevents_publication_and_clone(self):
        self.remote("courses", "DSCI_511_material_students", "remote\n")
        self.records["courses"].append({"name": "DSCI_512_broken_students"})
        result = self.run_sync()
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.root / "DSCI_511").exists())
        self.assertFalse((self.module / "current.txt").exists())

    def test_manifest_publication_failure_does_not_fetch_or_reset(self):
        source, remote = self.remote("courses", "DSCI_511_material_students", "old\n")
        target = self.root / "DSCI_511/official/current/DSCI_511_material_students"
        target.parent.mkdir(parents=True)
        self.git(self.root, "clone", "-q", str(remote), str(target))
        old = self.git(target, "rev-parse", "HEAD")
        self.advance(source, remote, "new\n")
        (self.module / "public.txt").mkdir()
        result = self.run_sync()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.git(target, "rev-parse", "HEAD"), old)
        self.assertEqual(self.git(target, "rev-parse", "origin/main"), old)
        self.assertEqual((target / "README.md").read_text(), "old\n")
        self.assertEqual(list(self.module.glob(".sync-manifests-*")), [])

    def test_git_failure_reports_error_but_later_repository_is_synced(self):
        missing = self.root / "remotes/courses/DSCI_510_missing_students.git"
        self.records["courses"].append({"name": "DSCI_510_missing_students", "clone_url": missing.as_uri()})
        self.remote("courses", "DSCI_511_safe_students", "safe\n")
        result = self.run_sync()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("DSCI_510_missing_students", result.stderr)
        self.assertEqual((self.root / "DSCI_511/official/current/DSCI_511_safe_students/README.md").read_text(), "safe\n")

    def test_local_path_and_file_url_origins_are_equivalent(self):
        source, remote = self.remote("courses", "DSCI_511_material_students", "old\n")
        target = self.root / "DSCI_511/official/current/DSCI_511_material_students"
        target.parent.mkdir(parents=True)
        self.git(self.root, "clone", "-q", str(remote), str(target))
        new = self.advance(source, remote, "new\n")
        result = self.run_sync()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.git(target, "rev-parse", "HEAD"), new)
        self.assertEqual((target / "README.md").read_text(), "new\n")

    def test_removed_arguments_fail_before_discovery(self):
        for argument in ("--offline", "--list-only", "--clean", "assignments", "--unknown"):
            with self.subTest(argument=argument):
                result = self.run_sync(argument)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(self.requests, [])
                self.assertFalse((self.module / "current.txt").exists())


if __name__ == "__main__":
    unittest.main()
