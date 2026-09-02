# Root Course Layout Design

## Intent

Make each active course directory the real daily working area. The root should show course work first, not source buckets.

No wrapper directory:

```text
DSCI_511/
DSCI_521/
DSCI_523/
DSCI_551/
admin/
README.md
pyproject.toml
uv.lock
.python-version
.gitignore
```

## Goal

Opening `DSCI_523/` or `DSCI_511/` shows that course's notes, official material clones, assignment work repositories, and course projects without jumping across `my_notes/`, `resources/`, `assignments/`, and `project/`.

## Non-goals

- Do not create empty root directories for future courses.
- Do not keep a `shared/`, `global/`, or `program/` bucket.
- Do not flatten nested Git repositories into the main repository.
- Do not rename official upstream repository directories.
- Do not merge private current-year material with public historical material.

## Current Evidence

Current layout is source/type-first:

```text
my_notes/courses/DSCI_523/
resources/mds-2026-27/DSCI_523_r-prog_students/
resources/ubc-mds/DSCI_523_r-prog/
assignments/DSCI_523_lab1_yz2000/
project/2026-09-01 DSCI 523 lec01-readr-dplyr-tidyr/
```

The user's notes already organize by use, not upstream structure. `my_notes/courses/DSCI_523/resources.md` says paths are relative to repo root and classifies material by "我拿它干什么". `resources/index.md` says it records locations, not content.

Current sync contracts depend on fixed paths:

- `sources.conf` sends current-year mirrors to `resources/mds-2026-27`.
- `sources.conf` sends public mirrors to `resources/ubc-mds`.
- `sources.conf` sends personal assignment work repositories to `assignments`.
- `.gitignore` ignores those three physical areas.
- `sync_course_repos.sh` clones to `<dest>/<repo>`.

A physical migration must update these contracts; a directory move alone is wrong.

## Target Root Layout

```text
DSCI_511/
DSCI_521/
DSCI_523/
DSCI_551/
admin/
tmp/
.superpowers/
.claude/
README.md
pyproject.toml
uv.lock
.python-version
.gitignore
```

Only courses with active local material get root directories in this migration. Public reference mirrors for future/inactive courses stay under `admin/upstream/public/` until they become active work.

## Course Layout

Example:

```text
DSCI_523/
  README.md
  notes/
    resources.md
    messages.md
    L01.md
  official/
    current/
      DSCI_523_r-prog_students/
    public/
      DSCI_523_r-prog/
  assignments/
    lab1/
      DSCI_523_lab1_yz2000/
    worksheet1/
      DSCI_523_worksheet1_yz2000/
  projects/
    2026-08-31 self-learning-demo/
    2026-09-01 lec01-readr-dplyr-tidyr/
```

Rules:

- `README.md`: short course landing page; navigation, current work, platform links, safe-edit notes.
- `notes/`: user-authored course notes and course-specific message archive.
- `official/current/`: current-year private/student mirror repos; sync may reset these.
- `official/public/`: public historical/reference mirror repos for active courses; sync may reset these.
- `assignments/`: personal assignment work repos; sync may fetch only, never reset or clean.
- `projects/`: user-created course demos/projects; move each project directory as a whole.

Move examples:

```text
my_notes/courses/DSCI_511/resources.md -> DSCI_511/notes/resources.md
resources/messages_by_courses/DSCI_523 -> DSCI_523/notes/messages.md
resources/mds-2026-27/DSCI_523_r-prog_students/ -> DSCI_523/official/current/DSCI_523_r-prog_students/
resources/ubc-mds/DSCI_523_r-prog/ -> DSCI_523/official/public/DSCI_523_r-prog/
assignments/DSCI_523_lab1_yz2000/ -> DSCI_523/assignments/lab1/DSCI_523_lab1_yz2000/
project/2026-09-01 DSCI 523 lec01-readr-dplyr-tidyr/ -> DSCI_523/projects/2026-09-01 lec01-readr-dplyr-tidyr/
```

## Admin Layout

`admin/` is the only non-course bucket. It contains repository maintenance, sync inputs, upstream caches not owned by active courses, and this repo's Python package code.

```text
admin/
  sources.conf
  sync_course_repos.sh
  cal_filter.py
  block-schedule-prompt.txt
  assignments.txt
  upstream/
    current/
      orientation/
      lab-sections/
      student-reps/
    public/
      <inactive-or-out-of-program public repos>/
  python/
    src/
      mdscl/
        __init__.py
```

Rules:

- No `shared/`. If content is course-specific, put it in that course. If not, it is maintenance/reference and goes under `admin/` or the root README.
- Root `README.md` absorbs the source map role from `resources/index.md`.
- `life` and other tiny non-course notes are folded into root `README.md` unless they grow enough to justify a named root file.
- `src/mdscl/` moves to `admin/python/src/mdscl/`. `pyproject.toml` must set `module-root = "admin/python/src"` under `[tool.uv.build-backend]`.

## Sync Routing Design

`sync_course_repos.sh` must route each repo name to a final path instead of cloning all repos under one source destination.

Routing:

```text
DSCI_523_r-prog_students      -> DSCI_523/official/current/DSCI_523_r-prog_students
DSCI_523_r-prog               -> DSCI_523/official/public/DSCI_523_r-prog
DSCI_523_lab1_yz2000          -> DSCI_523/assignments/lab1/DSCI_523_lab1_yz2000
orientation                   -> admin/upstream/current/orientation
DSCI_512_alg-data-struct      -> admin/upstream/public/DSCI_512_alg-data-struct
```

Course parsing:

- Match `^(DSCI|COLX)_[0-9]{3}` at the start of the repo name.
- That prefix is the root course directory name.
- Active course allowlist for this migration: `DSCI_511`, `DSCI_521`, `DSCI_523`, `DSCI_551`.
- Current-year course repos with an active course prefix route to `<COURSE>/official/current/<repo>`.
- Public repos with an active course prefix route to `<COURSE>/official/public/<repo>`.
- Public repos outside the active allowlist route to `admin/upstream/public/<repo>`.
- Current-year repos without a course prefix route to `admin/upstream/current/<repo>`.

Assignment parsing:

- Match `^(DSCI|COLX)_[0-9]{3}_(.+)_yz2000$`.
- The middle capture becomes the grouping directory, e.g. `lab1`, `worksheet1`, `lab0a`.
- Keep the full repo name as the clone directory.

## `sources.conf` Contract

Keep semicolon-delimited rows. Rename the `dest` concept to `family`; it selects routing behavior, not a literal clone destination.

```text
# name ; api_base ; org ; include ; exclude ; family ; mode
mds-2026-27 ; https://github.ubc.ca/api/v3 ; mds-2026-27 ;               ; _yz2000$ ; current ; mirror
ubc-mds     ; https://api.github.com       ; UBC-MDS     ; ^(DSCI|COLX)_ ;          ; public  ; mirror
assignments ; https://github.ubc.ca/api/v3 ; mds-2026-27 ; _yz2000$      ;          ; work    ; work
```

List snapshots should live under `admin/`:

```text
admin/current.txt
admin/public.txt
admin/work.txt
```

## `.gitignore` Contract

Do not ignore whole course directories. Ignore only nested cloned repositories and local generated state.

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

This keeps `DSCI_523/README.md`, `DSCI_523/notes/`, and `DSCI_523/projects/` tracked while avoiding accidental tracking of nested clones.

## Path Update Scope

Update tracked text references after moving files:

- moved `notes/resources.md` paths that currently reference `resources/mds-2026-27/...`;
- project READMEs with absolute paths under `/Users/youralmight/workspaces/reps/mdscl/project/...`;
- root `README.md` after absorbing `resources/index.md`;
- script comments/help text in `admin/sync_course_repos.sh`;
- `admin/sources.conf` comments;
- `.gitignore`;
- `pyproject.toml` for the new package source root.

Do not rewrite paths inside upstream mirror repositories unless needed for their own execution. They are upstream-owned.

## Migration Order

1. Create root directories for `DSCI_511`, `DSCI_521`, `DSCI_523`, and `DSCI_551`.
2. Move user-authored course notes and course message files into `<COURSE>/notes/`.
3. Move DSCI 523 projects into `DSCI_523/projects/`, preserving each project as a whole directory.
4. Move current-year active course mirrors into `<COURSE>/official/current/`.
5. Move public active-course mirrors into `<COURSE>/official/public/`.
6. Move assignment work repositories into `<COURSE>/assignments/<kind>/`.
7. Move non-course current-year upstream repos into `admin/upstream/current/`.
8. Move inactive public upstream repos into `admin/upstream/public/`.
9. Move operational tooling and Python package code into `admin/`.
10. Update `.gitignore`, `pyproject.toml`, sync routing, and tracked text references.
11. Verify sync routing, package import, stale paths, and project behavior.

## Verification

Minimum checks after implementation:

1. Run `bash admin/sync_course_repos.sh --offline --list-only` and verify it reads `admin/sources.conf` and does not recreate old roots.
2. Run offline sync for each family and verify it looks for existing clones in new paths.
3. Check nested Git repositories remain nested and are not staged by the main repo.
4. Search tracked files for stale references to:
   - `my_notes/courses/`
   - `resources/mds-2026-27/`
   - `resources/ubc-mds/`
   - `assignments/DSCI_`
   - `/project/2026-`
   - `shared/`
5. Run `uv run mdscl` to verify the package still builds from `admin/python/src`.
6. Run or open the moved DSCI 523 project command from its new directory to confirm cwd-relative `data/...` paths still work.
7. Confirm root scan shows only active courses, `admin/`, project config, and harness/tmp files.

## Review Decisions Already Made

- No `courses/` wrapper.
- No `shared/` bucket.
- Active course directories live at repository root.
- `src/` is not top-level; package source moves under `admin/python/src/`.
- Public mirrors for inactive/future courses stay in `admin/upstream/public/` for now.
- Official upstream clone directory names stay unchanged.
