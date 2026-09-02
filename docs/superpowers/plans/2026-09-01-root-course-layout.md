# Root Course Layout Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Convert the repository from source/type-first organization into root-level active course workspaces, with no `courses/` wrapper and no `shared/` bucket.

**Architecture:** Active courses live at repository root (`DSCI_511/`, `DSCI_521/`, `DSCI_523/`, `DSCI_551/`). Each course owns notes, messages, official active-course upstream clones, assignment work clones, and user projects. All non-course maintenance and inactive upstream caches live under `admin/`; Python package source moves to `admin/python/src` and uv_build is configured with `module-root = "admin/python/src"`.

**Tech Stack:** Bash, Git nested repositories, uv/uv_build, Python package src layout, Markdown.

**Spec:** `docs/superpowers/specs/2026-09-01-root-course-layout-design.md`

## Global Constraints

- No `courses/`, `shared/`, `global/`, or `program/` wrapper/bucket.
- Create root course directories only for `DSCI_511`, `DSCI_521`, `DSCI_523`, and `DSCI_551` in this migration.
- Do not flatten nested Git repositories into the main repository.
- Do not rename official upstream repository clone directories.
- Do not reset, clean, merge, or switch branches inside assignment work repositories.
- Current/public upstream mirrors may be fetched/reset by the sync script; assignment repositories may only fetch.
- Keep `sources.conf` semicolon-delimited.
- Move `src/mdscl/` to `admin/python/src/mdscl/` and set `[tool.uv.build-backend].module-root = "admin/python/src"`.
- Use tool `grep` for stale path searches; do not use shell grep/rg.

## File Structure Map

**Create/move course roots:**

```text
DSCI_511/
DSCI_521/
DSCI_523/
DSCI_551/
```

Each course root has:

```text
README.md
notes/
official/current/
official/public/
assignments/<kind>/
projects/                 # only when the course has user projects
```

**Create/move admin:**

```text
admin/
  sources.conf
  sync_course_repos.sh
  cal_filter.py
  block-schedule-prompt.txt
  assignments.txt
  upstream/current/
  upstream/public/
  python/src/mdscl/
```

**Modify root files:**

```text
README.md
course-index.md
pyproject.toml
.gitignore
```

---

### Task 1: Move tracked course notes, messages, projects, and admin files

**Files:**
- Move: `my_notes/courses/index.md` -> `course-index.md`
- Move: `my_notes/courses/DSCI_511/` -> `DSCI_511/notes/`
- Move: `my_notes/courses/DSCI_521/` -> `DSCI_521/notes/`
- Move: `my_notes/courses/DSCI_523/` -> `DSCI_523/notes/`
- Move: `my_notes/courses/DSCI_551/` -> `DSCI_551/notes/`
- Move: `resources/messages_by_courses/DSCI_511` -> `DSCI_511/notes/messages.md`
- Move: `resources/messages_by_courses/DSCI_521` -> `DSCI_521/notes/messages.md`
- Move: `resources/messages_by_courses/DSCI_523` -> `DSCI_523/notes/messages.md`
- Move: `resources/messages_by_courses/DSCI_551` -> `DSCI_551/notes/messages.md`
- Move: `project/2026-08-31 DSCI 523 self-learning-demo/` -> `DSCI_523/projects/2026-08-31 self-learning-demo/`
- Move: `project/2026-09-01 DSCI 523 lec01-readr-dplyr-tidyr/` -> `DSCI_523/projects/2026-09-01 lec01-readr-dplyr-tidyr/`
- Move: `sources.conf`, `sync_course_repos.sh`, `cal_filter.py`, `block-schedule-prompt.txt`, `assignments.txt` -> `admin/`
- Move: `src/mdscl/` -> `admin/python/src/mdscl/`

**Interfaces:**
- Consumes: approved spec path and existing repository paths.
- Produces: root active-course directories and `admin/` skeleton used by later tasks.

- [ ] **Step 1: Create destination directories**

```bash
mkdir -p \
  DSCI_511/notes DSCI_511/official/current DSCI_511/official/public DSCI_511/assignments \
  DSCI_521/notes DSCI_521/official/current DSCI_521/official/public DSCI_521/assignments \
  DSCI_523/notes DSCI_523/official/current DSCI_523/official/public DSCI_523/assignments DSCI_523/projects \
  DSCI_551/notes DSCI_551/official/current DSCI_551/official/public DSCI_551/assignments \
  admin/upstream/current admin/upstream/public admin/python/src
```

- [ ] **Step 2: Move all-year index, course notes, and course messages with git**

```bash
git mv my_notes/courses/index.md course-index.md
git mv my_notes/courses/DSCI_511/* DSCI_511/notes/
git mv my_notes/courses/DSCI_521/* DSCI_521/notes/
git mv my_notes/courses/DSCI_523/* DSCI_523/notes/
git mv my_notes/courses/DSCI_551/* DSCI_551/notes/
git mv resources/messages_by_courses/DSCI_511 DSCI_511/notes/messages.md
git mv resources/messages_by_courses/DSCI_521 DSCI_521/notes/messages.md
git mv resources/messages_by_courses/DSCI_523 DSCI_523/notes/messages.md
git mv resources/messages_by_courses/DSCI_551 DSCI_551/notes/messages.md
```

- [ ] **Step 3: Move DSCI 523 user projects as whole directories**

```bash
git mv "project/2026-08-31 DSCI 523 self-learning-demo" "DSCI_523/projects/2026-08-31 self-learning-demo"
git mv "project/2026-09-01 DSCI 523 lec01-readr-dplyr-tidyr" "DSCI_523/projects/2026-09-01 lec01-readr-dplyr-tidyr"
```

- [ ] **Step 4: Move admin files and Python package source**

```bash
git mv sources.conf admin/sources.conf
git mv sync_course_repos.sh admin/sync_course_repos.sh
git mv cal_filter.py admin/cal_filter.py
git mv block-schedule-prompt.txt admin/block-schedule-prompt.txt
git mv assignments.txt admin/assignments.txt
git mv src/mdscl admin/python/src/mdscl
```

- [ ] **Step 5: Remove empty old tracked directories if present**

```bash
rmdir my_notes/courses my_notes resources/messages_by_courses project src 2>/dev/null || true
```

- [ ] **Step 6: Verify moved tracked files exist**

```bash
test -f DSCI_523/notes/resources.md
test -f DSCI_523/notes/messages.md
test -f "DSCI_523/projects/2026-09-01 lec01-readr-dplyr-tidyr/README.md"
test -f admin/sources.conf
test -f admin/sync_course_repos.sh
test -f admin/python/src/mdscl/__init__.py
```

- [ ] **Step 7: Commit tracked move shell**

```bash
git add -A
git commit -m "refactor: create root course workspaces"
```

---

### Task 2: Move ignored nested Git repositories into course/admin locations

**Files:**
- Move ignored dirs under `resources/mds-2026-27/`.
- Move ignored dirs under `resources/ubc-mds/`.
- Move ignored dirs under `assignments/`.

**Interfaces:**
- Consumes: destinations created by Task 1.
- Produces: nested Git clones at paths consumed by sync routing.

- [ ] **Step 1: Move current-year active course mirrors**

```bash
mv resources/mds-2026-27/DSCI_511_py-prog_students DSCI_511/official/current/
mv resources/mds-2026-27/DSCI_521_platforms-dsci_students DSCI_521/official/current/
mv resources/mds-2026-27/DSCI_523_r-prog_students DSCI_523/official/current/
mv resources/mds-2026-27/DSCI_551_stat-prob-dsci_students DSCI_551/official/current/
```

- [ ] **Step 2: Move program-level current-year mirrors to admin**

```bash
mv resources/mds-2026-27/orientation admin/upstream/current/
mv resources/mds-2026-27/lab-sections admin/upstream/current/
mv resources/mds-2026-27/student-reps admin/upstream/current/
```

- [ ] **Step 3: Move active-course public mirrors**

```bash
mv resources/ubc-mds/DSCI_511_prog-dsci DSCI_511/official/public/
mv resources/ubc-mds/DSCI_521_platforms-dsci DSCI_521/official/public/
mv resources/ubc-mds/DSCI_521_platforms-dsci_book DSCI_521/official/public/
mv resources/ubc-mds/DSCI_523_r-prog DSCI_523/official/public/
mv resources/ubc-mds/DSCI_551_stat-prob-dsci DSCI_551/official/public/
```

- [ ] **Step 4: Move remaining public mirrors to admin**

```bash
mkdir -p admin/upstream/public
for d in resources/ubc-mds/*; do [ -e "$d" ] && mv "$d" admin/upstream/public/; done
```

- [ ] **Step 5: Move assignment work repositories**

```bash
mkdir -p \
  DSCI_511/assignments/lab1 DSCI_511/assignments/worksheet1 \
  DSCI_521/assignments/lab0a DSCI_521/assignments/lab0b \
  DSCI_523/assignments/lab1 DSCI_523/assignments/worksheet1 \
  DSCI_551/assignments/lab1
mv assignments/DSCI_511_lab1_yz2000 DSCI_511/assignments/lab1/
mv assignments/DSCI_511_worksheet1_yz2000 DSCI_511/assignments/worksheet1/
mv assignments/DSCI_521_lab0a_yz2000 DSCI_521/assignments/lab0a/
mv assignments/DSCI_521_lab0b_yz2000 DSCI_521/assignments/lab0b/
mv assignments/DSCI_523_lab1_yz2000 DSCI_523/assignments/lab1/
mv assignments/DSCI_523_worksheet1_yz2000 DSCI_523/assignments/worksheet1/
mv assignments/DSCI_551_lab1_yz2000 DSCI_551/assignments/lab1/
```

- [ ] **Step 6: Verify nested Git boundaries survived**

```bash
test -d DSCI_523/official/current/DSCI_523_r-prog_students/.git
test -d DSCI_523/official/public/DSCI_523_r-prog/.git
test -d DSCI_523/assignments/lab1/DSCI_523_lab1_yz2000/.git
test -d admin/upstream/current/orientation/.git
test -d admin/upstream/public/DSCI_512_alg-data-struct/.git
```

- [ ] **Step 7: Leave this task uncommitted until `.gitignore` is updated in Task 3**

No commit here. These dirs are ignored only after Task 3 updates `.gitignore`.

---

### Task 3: Update ignore rules and package source configuration

**Files:**
- Modify: `.gitignore`
- Modify: `pyproject.toml`

**Interfaces:**
- Consumes: moved nested repos from Task 2 and package source from Task 1.
- Produces: main repository ignores nested clones and uv can build/import `mdscl` from `admin/python/src`.

- [ ] **Step 1: Replace `.gitignore` clone rules**

Use this exact clone section:

```gitignore
# Upstream clones and personal assignment repos are nested Git repositories.
DSCI_*/official/current/*/
DSCI_*/official/public/*/
DSCI_*/assignments/*/*/
COLX_*/official/current/*/
COLX_*/official/public/*/
COLX_*/assignments/*/*/
admin/upstream/current/*/
admin/upstream/public/*/

.DS_Store
```

- [ ] **Step 2: Add uv_build module root to `pyproject.toml`**

Add this table after `[build-system]`:

```toml
[tool.uv.build-backend]
module-root = "admin/python/src"
```

Keep the existing project metadata and script entry point:

```toml
[project.scripts]
mdscl = "mdscl:main"
```

- [ ] **Step 3: Verify package import and console script**

```bash
uv run python -c 'import mdscl; print(mdscl.__name__)'
uv run mdscl
```

Expected output includes:

```text
mdscl
Hello from mdscl!
```

- [ ] **Step 4: Verify nested clones are not staged by the main repo**

```bash
git status --short --ignored
```

Expected: course notes/projects/admin file changes may appear; nested clone directories appear as ignored (`!!`) or do not appear as tracked additions. No `?? DSCI_523/official/current/DSCI_523_r-prog_students/...` file flood.

- [ ] **Step 5: Commit ignore/package changes together with ignored-dir moves if needed**

```bash
git add .gitignore pyproject.toml
git commit -m "chore: route package and clone ignores through admin"
```

---

### Task 4: Rewrite sync routing for root course layout

**Files:**
- Modify: `admin/sources.conf`
- Modify: `admin/sync_course_repos.sh`

**Interfaces:**
- Consumes: new physical clone locations from Tasks 1-2.
- Produces: sync script that discovers the same upstream repos and maps each repo to its new course/admin path.

- [ ] **Step 1: Update `admin/sources.conf` header and rows**

Use this table shape:

```text
# name ; api_base ; org ; include ; exclude ; family ; mode
mds-2026-27 ; https://github.ubc.ca/api/v3 ; mds-2026-27 ;               ; _yz2000$ ; current ; mirror
ubc-mds     ; https://api.github.com       ; UBC-MDS     ; ^(DSCI|COLX)_ ;          ; public  ; mirror
assignments ; https://github.ubc.ca/api/v3 ; mds-2026-27 ; _yz2000$      ;          ; work    ; work
```

- [ ] **Step 2: Change root/config resolution at the top of `admin/sync_course_repos.sh`**

Replace the current root/config initialization with:

```bash
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "$script_dir/.." && pwd)"
conf="$script_dir/sources.conf"
[[ -f "$conf" ]] || { echo "缺来源配置: $conf" >&2; exit 1; }
```

- [ ] **Step 3: Add routing helpers before the main `while IFS=';'` loop**

```bash
course_prefix() {
  local repo="$1"
  if [[ "$repo" =~ ^(DSCI|COLX)_[0-9]{3} ]]; then
    printf '%s' "${BASH_REMATCH[0]}"
  fi
}

assignment_kind() {
  local repo="$1"
  if [[ "$repo" =~ ^(DSCI|COLX)_[0-9]{3}_(.+)_yz2000$ ]]; then
    printf '%s' "${BASH_REMATCH[2]}"
  fi
}

active_course() {
  local course="$1"
  [[ -n "$course" && -d "$repo_root/$course" ]]
}

repo_dest() {
  local family="$1" repo="$2" course kind
  course="$(course_prefix "$repo")"
  case "$family" in
    current)
      if active_course "$course"; then
        printf '%s/%s/official/current/%s' "$repo_root" "$course" "$repo"
      else
        printf '%s/admin/upstream/current/%s' "$repo_root" "$repo"
      fi
      ;;
    public)
      if active_course "$course"; then
        printf '%s/%s/official/public/%s' "$repo_root" "$course" "$repo"
      else
        printf '%s/admin/upstream/public/%s' "$repo_root" "$repo"
      fi
      ;;
    work)
      kind="$(assignment_kind "$repo")"
      [[ -n "$course" && -n "$kind" ]] || { echo "无法路由作业仓库: $repo" >&2; return 1; }
      printf '%s/%s/assignments/%s/%s' "$repo_root" "$course" "$kind" "$repo"
      ;;
    *)
      echo "未知 family: $family" >&2
      return 1
      ;;
  esac
}
```

- [ ] **Step 4: Parse `family` instead of `dest` in the main loop**

Change loop variables and validation from `dest` to `family`:

```bash
while IFS=';' read -r name api org inc exc family mode; do
  name="$(trim "${name:-}")"
  [[ -z "$name" || "$name" == \#* ]] && continue
  api="$(trim "${api:-}")";  org="$(trim "${org:-}")"
  inc="$(trim "${inc:-}")";  exc="$(trim "${exc:-}")"
  family="$(trim "${family:-}")"; mode="$(trim "${mode:-mirror}")"

  [[ -n "$family" ]] || { echo "来源 $name 没写 family" >&2; failed+=("family $name"); continue; }
```

- [ ] **Step 5: Write list snapshots under `admin/`**

Replace list path setup with:

```bash
list="$script_dir/$family.txt"
```

The expected snapshots are:

```text
admin/current.txt
admin/public.txt
admin/work.txt
```

- [ ] **Step 6: Use routed destination per repo**

Inside `while read -r url`, replace `dir="$dest_abs/$repo"` with:

```bash
dir="$(repo_dest "$family" "$repo")" || { failed+=("route $url"); continue; }
```

Before clone, ensure parent exists:

```bash
mkdir -p "$(dirname "$dir")"
```

Update status output from `→ $dest` to:

```bash
echo "=== $name [$mode/$family] ($(grep -cve '^\s*$' -e '^#' "$list") 个仓库)"
```

If implementing inside this harness, replace the shell `grep -cve` with a non-grep count command or a small Python one-liner to respect tool policy.

- [ ] **Step 7: Remove stale cleanup of old resource list files**

Delete these old-root cleanup lines:

```bash
rm resources/mds-2026-27.txt
rm resources/ubc-mds.txt
```

- [ ] **Step 8: Verify list-only mode without network clone/fetch**

```bash
bash admin/sync_course_repos.sh --offline --list-only
```

Expected: command reads `admin/sources.conf`. It must not complain about missing root `sources.conf` or recreate `resources/` / `assignments/`.

- [ ] **Step 9: Commit sync routing**

```bash
git add admin/sources.conf admin/sync_course_repos.sh admin/current.txt admin/public.txt admin/work.txt
git commit -m "refactor: route synced repos into course roots"
```

---

### Task 5: Update root README and moved course/project references

**Files:**
- Modify: `README.md`
- Modify: `DSCI_511/notes/resources.md`
- Modify: `DSCI_521/notes/resources.md`
- Modify: `DSCI_523/notes/resources.md`
- Modify: `DSCI_551/notes/resources.md`
- Modify: `DSCI_523/projects/2026-08-31 self-learning-demo/README.md`
- Move/remove after content is preserved in `README.md`: `resources/index.md`
- Move/remove after content is preserved in `README.md`: `resources/messages_by_courses/life`
- Move/remove after content is preserved in `README.md`: `resources/messages_by_courses/quiz_and_cheetsheet_details.txt`
- Modify: `DSCI_523/projects/2026-09-01 lec01-readr-dplyr-tidyr/README.md`

**Interfaces:**
- Consumes: final physical paths.
- Produces: tracked docs that point at the new layout and do not preserve old mental model.

- [ ] **Step 1: Replace root README with the source-map content and new layout contract**

Use these sections:

```markdown
# MDS-CL workspace

Top level is course-first. Open a `DSCI_*` directory for daily study.

## Active courses

- `DSCI_511/` — Programming for Data Science
- `DSCI_521/` — Computing Platforms for Data Science
- `DSCI_523/` — Programming for Data Manipulation
- `DSCI_551/` — Descriptive Statistics and Probability
- `course-index.md` — all-year course table

## Directory rules

- Course-specific notes, messages, official material, assignments, and projects live in the course directory.
- `admin/` contains sync tooling, inactive upstream caches, calendar tooling, and Python package source.
- No `shared/` bucket. If material belongs to a course, put it there; otherwise keep it in `admin/` or this README.

## Sources

- Canvas: https://canvas.ubc.ca/
- Current-year GitHub Enterprise org: https://github.ubc.ca/MDS-2026-27
- Public historical UBC-MDS org: https://github.com/UBC-MDS
- MDS-CL project site: https://ubc-mdscl.github.io/
- CL calendar: https://ling.air.arts.ubc.ca/mds-cl-calendar/

Use `admin/sync_course_repos.sh` with `admin/sources.conf` to update upstream clones.
```

Then remove old source/message files after preserving their useful content in `README.md`:

```bash
git rm resources/index.md
git rm resources/messages_by_courses/life
git rm resources/messages_by_courses/quiz_and_cheetsheet_details.txt
```

- [ ] **Step 2: Update course note paths**

Replace old paths with new paths:

```text
resources/mds-2026-27/DSCI_511_py-prog_students/ -> ../official/current/DSCI_511_py-prog_students/
resources/mds-2026-27/DSCI_523_r-prog_students/ -> ../official/current/DSCI_523_r-prog_students/
resources/mds-2026-27/DSCI_551_stat-prob-dsci_students/ -> ../official/current/DSCI_551_stat-prob-dsci_students/
my_notes/courses/index.md -> ../../course-index.md
```

- [ ] **Step 3: Update DSCI 523 project README open commands**

Use new absolute paths:

```bash
cursor "/Users/youralmight/workspaces/reps/mdscl/DSCI_523/projects/2026-08-31 self-learning-demo"
codium "/Users/youralmight/workspaces/reps/mdscl/DSCI_523/projects/2026-09-01 lec01-readr-dplyr-tidyr"
```

- [ ] **Step 4: Use Grep tool to find stale tracked references**

Search tracked/non-ignored content for:

```text
my_notes/courses/
resources/mds-2026-27/
resources/ubc-mds/
assignments/DSCI_
/project/2026-
shared/
src/mdscl
```

Acceptable hits: historical evidence in the design spec and implementation plan only. Fix hits in active docs/scripts.

- [ ] **Step 5: Commit documentation/reference updates**

```bash
git add README.md course-index.md DSCI_*/notes/*.md DSCI_523/projects/*/README.md
git commit -m "docs: update paths for root course layout"
```

---

### Task 6: Final verification and cleanup

**Files:**
- Verify whole repository state.
- Modify only if verification finds stale paths or accidental tracked clone files.

**Interfaces:**
- Consumes: completed migration.
- Produces: verified layout ready for normal use.

- [ ] **Step 1: Verify root layout is course-first**

Use Read tool on repository root. Expected visible roots include active courses and `admin/`; old roots `my_notes/`, `resources/`, `assignments/`, `project/`, and top-level `src/` should be absent unless empty removal failed.

- [ ] **Step 2: Verify package command**

```bash
uv run mdscl
```

Expected:

```text
Hello from mdscl!
```

- [ ] **Step 3: Verify sync script offline list mode**

```bash
bash admin/sync_course_repos.sh --offline --list-only
```

Expected: exits successfully using `admin/*.txt` lists and `admin/sources.conf`.

- [ ] **Step 4: Verify assignment work repo was not reset or cleaned**

```bash
git -C DSCI_523/assignments/lab1/DSCI_523_lab1_yz2000 status --short
git -C DSCI_523/assignments/worksheet1/DSCI_523_worksheet1_yz2000 status --short
```

Expected: whatever local work existed remains; no command in this plan resets or cleans these repos.

- [ ] **Step 5: Verify DSCI 523 project cwd-relative data path**

```bash
cd "DSCI_523/projects/2026-09-01 lec01-readr-dplyr-tidyr"
test -d data
test -f README.md
test -f lec01-demo.ipynb
```

- [ ] **Step 6: Use Grep tool for stale paths one last time**

Patterns:

```text
my_notes/courses/|resources/mds-2026-27/|resources/ubc-mds/|assignments/DSCI_|/project/2026-|shared/|src/mdscl
```

Acceptable hits: spec/plan historical sections only. No active script or course note should point at old paths.

- [ ] **Step 7: Check main repo staging**

```bash
git status --short --ignored
```

Expected: no flood of files from nested clones as untracked additions. Ignored clone roots may appear as `!!`.

- [ ] **Step 8: Commit final fixes if any**

```bash
git add -A
git commit -m "chore: finish root course layout migration"
```

Skip this commit if Step 7 has nothing new to commit.
