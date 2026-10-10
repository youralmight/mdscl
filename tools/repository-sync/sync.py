import argparse
import json
import re
import subprocess
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


def git(directory: Path, *arguments: str) -> str:
    try:
        result = subprocess.run(
            ["git", "-C", str(directory), *arguments],
            capture_output=True, text=True, timeout=120,
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(f"Git {arguments[0]} timed out: {directory}") from exc
    if result.returncode:
        detail = result.stderr.strip() or result.stdout.strip()
        raise RuntimeError(
            f"Git {arguments[0]} failed: {directory} (exit {result.returncode})\n{detail}"
        )
    return result.stdout.strip()


def origin_identity(url: str) -> tuple:
    scp = re.match(r"^(?:[^@/]+@)?([^:/]+):(.+)$", url)
    if scp and "://" not in url:
        host, path = scp.groups()
        return "github", host.casefold(), urllib.parse.unquote(path).strip("/").removesuffix(".git").casefold()
    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme in ("https", "ssh"):
        host = (parsed.hostname or "").casefold()
        if parsed.port and not (parsed.scheme == "https" and parsed.port == 443):
            host += f":{parsed.port}"
        return "github", host, urllib.parse.unquote(parsed.path).strip("/").removesuffix(".git").casefold()
    if parsed.scheme == "file":
        return "file", str(Path(urllib.parse.unquote(parsed.path)).resolve())
    if not parsed.scheme and not parsed.netloc:
        return "file", str(Path(url).resolve())
    return parsed.scheme.casefold(), parsed.netloc.casefold(), parsed.path.rstrip("/"), parsed.query, parsed.fragment


def discover(api: str, org: str, token: str):
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"token {token}"
    page = 1
    while True:
        endpoint = f"{api}/orgs/{org}/repos?per_page=100&page={page}"
        request = urllib.request.Request(endpoint, headers=headers)
        try:
            with urllib.request.urlopen(request, timeout=120) as response:
                data = json.load(response)
        except (urllib.error.URLError, OSError, ValueError) as exc:
            raise RuntimeError(f"API discovery failed: {endpoint}: {exc}") from exc
        if not isinstance(data, list):
            raise ValueError(f"API response is not a repository list: {endpoint}")
        for repository in data:
            if (not isinstance(repository, dict)
                    or not isinstance(repository.get("name"), str)
                    or not isinstance(repository.get("clone_url"), str)):
                raise ValueError(f"invalid repository entry: {endpoint}")
            yield repository
        if len(data) < 100:
            return
        page += 1


def update_checkout(target: Path, url: str, mode: str) -> None:
    # Clone missing current materials and personal assignments.
    if not (target / ".git").is_dir():
        target.parent.mkdir(parents=True, exist_ok=True)
        git(target.parent, "clone", "--quiet", url, str(target))
        print(f"  cloned {target.name}", flush=True)
        return

    # Fetch first; resolve the remote branch without guessing another source.
    git(target, "fetch", "--quiet", "--prune", "--tags", "--force", "origin")
    remote_ref = subprocess.run(
        ["git", "-C", str(target), "symbolic-ref", "--quiet", "--short", "refs/remotes/origin/HEAD"],
        capture_output=True, text=True, timeout=120,
    )
    if remote_ref.returncode == 1:
        git(target, "remote", "set-head", "origin", "--auto")
        head = git(target, "symbolic-ref", "--quiet", "--short", "refs/remotes/origin/HEAD")
    elif remote_ref.returncode:
        raise RuntimeError(f"cannot resolve origin/HEAD: {target}\n{remote_ref.stderr.strip()}")
    else:
        head = remote_ref.stdout.strip()
    old = git(target, "rev-parse", "HEAD")
    new = git(target, "rev-parse", head)

    # Official mirrors align to origin; unchanged mirrors retain local edits.
    if mode == "mirror":
        if old != new:
            git(target, "reset", "--quiet", "--hard", new)
            print(f"  aligned {old[:8]} -> {new[:8]}", flush=True)
        dirty = git(target, "status", "--porcelain")
        if dirty:
            print(f"  warning: remaining local changes retained:\n{dirty}", flush=True)
    else:
        count = int(git(target, "rev-list", "--count", f"{old}..{new}"))
        if count:
            branch = git(target, "rev-parse", "--abbrev-ref", "HEAD")
            print(f"  {head}: {count} new commits; {branch} and working tree preserved", flush=True)
            print(f"  merge manually: git -C '{target}' merge {head}", flush=True)


# uv run --project ../uv_base python tools/repository-sync/sync.py
def main() -> int:
    argparse.ArgumentParser(description="Sync all configured course repositories from origin.").parse_args()
    module = Path(__file__).resolve().parent
    root = module.parent.parent

    # Load source policy and API credentials once.
    sources = []
    names = set()
    for number, line in enumerate((module / "sources.conf").read_text().splitlines(), 1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        fields = [field.strip() for field in line.split(";")]
        if len(fields) != 7:
            raise ValueError(f"sources.conf line {number}: expected seven semicolon-separated fields")
        name, api, org, include, exclude, family, mode = fields
        if not name or not api or not org or name in names:
            raise ValueError(f"invalid or duplicate source: {name!r} (line {number})")
        if family not in {"current", "public", "work"} or mode not in {"mirror", "work"}:
            raise ValueError(f"invalid family/mode: {name} ({family}/{mode})")
        names.add(name)
        sources.append((name, api.rstrip("/"), org, re.compile(include), re.compile(exclude) if exclude else None, family, mode))
    if not sources:
        raise ValueError(f"empty source configuration: {module / 'sources.conf'}")
    credentials = {}
    credential_file = Path.home() / ".git-credentials"
    if credential_file.exists():
        for line in credential_file.read_text().splitlines():
            parsed = urllib.parse.urlsplit(line)
            if parsed.hostname and parsed.password:
                credentials.setdefault(parsed.hostname, urllib.parse.unquote(parsed.password))

    # Discover all sources and build one in-memory execution plan.
    plan = {}
    snapshots = {family: set() for family in ("current", "work", "public")}
    for name, api, org, include, exclude, family, mode in sources:
        host = urllib.parse.urlsplit(api).hostname
        print(f"discover {name}: {org}", flush=True)
        for repository in discover(api, org, credentials.get(host, "")):
            repo, url = repository["name"], repository["clone_url"]
            if not include.search(repo) or (exclude is not None and exclude.search(repo)):
                continue
            snapshots[family].add(url)
            course = re.match(r"^(DSCI|COLX)_[0-9]{3}", repo)
            if family == "work":
                assignment = re.fullmatch(r"((?:DSCI|COLX)_[0-9]{3})_(.+)_yz2000", repo)
                if assignment is None:
                    raise ValueError(f"cannot route assignment repository: {repo} ({name})")
                target = root / assignment[1] / "assignments" / assignment[2] / repo
            else:
                if course is None:
                    continue
                target = root / course[0] / "official" / family / repo
                if family == "public" and not (target / ".git").is_dir():
                    continue
            if target in plan and plan[target][0] != url:
                previous_url, previous_source, _, _ = plan[target]
                raise ValueError(
                    f"target conflict: {target}\n  {previous_source}: {previous_url}\n  {name}: {url}"
                )
            if target not in plan:
                plan[target] = url, name, family, mode

    # Validate every retained checkout before any fetch, reset or publication.
    errors = []
    for target, (url, name, _, _) in sorted(plan.items()):
        if not target.exists() and not target.is_symlink():
            continue
        if not (target / ".git").is_dir():
            errors.append(f"target exists but is not a Git repository: {target} ({name})")
            continue
        try:
            actual = git(target, "remote", "get-url", "origin")
            if origin_identity(url) != origin_identity(actual):
                errors.append(f"origin mismatch: {target} ({name})\n  configured: {url}\n  existing: {actual}")
        except (OSError, RuntimeError, ValueError) as exc:
            errors.append(str(exc))
    if errors:
        raise ValueError("origin validation failed; no sync performed\n" + "\n".join(errors))

    # Stage complete URL inventories; publication failure prevents Git updates.
    with tempfile.TemporaryDirectory(prefix=".sync-manifests-", dir=module) as staging:
        for family, urls in snapshots.items():
            Path(staging, f"{family}.txt").write_text("".join(f"{url}\n" for url in sorted(urls)))
        for family in snapshots:
            Path(staging, f"{family}.txt").replace(module / f"{family}.txt")

    # Apply independent targets; report every failure without rollback.
    failures = []
    for target, (url, name, family, mode) in sorted(plan.items()):
        print(f"=== {name} [{mode}/{family}] {target.name}", flush=True)
        try:
            update_checkout(target, url, mode)
        except (OSError, RuntimeError, ValueError, subprocess.TimeoutExpired) as exc:
            failure = f"{target}: {exc}"
            failures.append(failure)
            print(f"FAILED: {failure}", file=sys.stderr, flush=True)
    if failures:
        print(f"failed {len(failures)} repositories; successful updates were not rolled back", file=sys.stderr)
        for failure in failures:
            print(failure, file=sys.stderr)
        return 1
    print(f"all successful: {len(plan)} repositories")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, RuntimeError, ValueError) as exc:
        print(f"sync failed: {exc}", file=sys.stderr)
        sys.exit(1)
