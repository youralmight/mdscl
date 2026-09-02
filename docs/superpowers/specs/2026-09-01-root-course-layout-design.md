# Root Course Layout Design

## Intent

Make each active course directory a real daily working area. The top level should answer "which course am I working on now?" before it answers "what type/source of file is this?".

This design intentionally removes the extra `courses/` wrapper. Course directories live directly at repository root:

```text
DSCI_511/
DSCI_521/
DSCI_523/
DSCI_551/
shared/
admin/
src/
tmp/
pyproject.toml
uv.lock
README.md
```

## Goal

After migration, opening `DSCI_523/` or `DSCI_511/` should show the course's notes, official material clones, assignment work repositories, and course projects without jumping across `my_notes/`, `resources/`, `assignments/`, and `project/`.

## Non-goals

- Do not create empty top-level directories for all 25 future courses.
- Do not flatten nested Git repositories into the main repository.
- Do not rename official upstream repository directories.
- Do not merge private current-year material with public historical material.
- Do not treat generated PDFs, rendered websites, or submission zips as duplicates unless they already live inside the assignment/project repo being moved as a unit.

## Current Evidence

The current repository is source/type-first:

```text
my_notes/courses/DSCI_523/
resources/mds-2026-27/DSCI_523_r-prog_students/
resources/ubc-mds/DSCI_523_r-prog/
assignments/DSCI_523_lab1_yz2000/
project/2026-09-01 DSCI 523 lec01-readr-dplyr-tidyr/
```

The user's notes already organize material by use, not by upstream layout. For example, `my_notes/courses/DSCI_523/resources.md` says paths are relative to the repository root and classifies material by "我拿它干什么". `resources/index.md` says it records locations, not content, and that concrete content belongs under `my_notes/`.

Sync contracts currently depend on fixed paths:

- `sources.conf` sends current-year mirrors to `resources/mds-2026-27`.
- `sources.conf` sends public mirrors to `resources/ubc-mds`.
- `sources.conf` sends personal assignment work repositories to `assignments`.
- `.gitignore` ignores those three physical areas.
- `sync_course_repos.sh` assumes one destination root per source and clones to `<dest>/<repo>`.

A physical course-first migration must update these contracts; a plain directory move is not enough.

## Target Top-Level Layout

```text
DSCI_511/
DSCI_521/
DSCI_523/
DSCI_551/
shared/
admin/
src/
tmp/
.superpowers/
.claude/
README.md
pyproject.toml
uv.lock
.python-version
.gitignore
```

Root course directories are created only for courses with active local working material in this migration. Existing public reference mirrors for inactive/future courses remain under `shared/resources/ubc-mds/` until those courses become active working areas.

Rationale: the real need is daily study, not a decorative year archive. Empty or rarely used root course directories add scanning noise.

## Per-Course Layout

Example for `DSCI_523`:

```text
DSCI_523/
  README.md
  notes/
    resources.md
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

### `README.md`

Course landing page maintained by this repository. It should contain only high-value navigation:

- what this course is about;
- current active work;
- links to `notes/resources.md`;
- platform links and deadline source;
- which directories are safe to edit;
- which directories are upstream clones or generated output.

It must not duplicate full syllabus tables or upstream README content.

### `notes/`

User-authored notes and course-specific resource maps. Move from `my_notes/courses/<COURSE>/`.

Examples:

```text
my_notes/courses/DSCI_511/resources.md -> DSCI_511/notes/resources.md
my_notes/courses/DSCI_523/L01.md -> DSCI_523/notes/L01.md
```

### `official/current/`

Current-year private/student upstream repositories. These are mirror repositories; local edits may be destroyed by sync.

Examples:

```text
resources/mds-2026-27/DSCI_511_py-prog_students/ -> DSCI_511/official/current/DSCI_511_py-prog_students/
resources/mds-2026-27/DSCI_523_r-prog_students/ -> DSCI_523/official/current/DSCI_523_r-prog_students/
resources/mds-2026-27/DSCI_551_stat-prob-dsci_students/ -> DSCI_551/official/current/DSCI_551_stat-prob-dsci_students/
resources/mds-2026-27/DSCI_521_platforms-dsci_students/ -> DSCI_521/official/current/DSCI_521_platforms-dsci_students/
```

### `official/public/`

Public historical/reference upstream repositories for an active course. These are also mirror repositories.

Examples:

```text
resources/ubc-mds/DSCI_511_prog-dsci/ -> DSCI_511/official/public/DSCI_511_prog-dsci/
resources/ubc-mds/DSCI_523_r-prog/ -> DSCI_523/official/public/DSCI_523_r-prog/
resources/ubc-mds/DSCI_551_stat-prob-dsci/ -> DSCI_551/official/public/DSCI_551_stat-prob-dsci/
resources/ubc-mds/DSCI_521_platforms-dsci/ -> DSCI_521/official/public/DSCI_521_platforms-dsci/
resources/ubc-mds/DSCI_521_platforms-dsci_book/ -> DSCI_521/official/public/DSCI_521_platforms-dsci_book/
```

Public repos for non-active courses remain in `shared/resources/ubc-mds/` in this migration.

### `assignments/`

Personal assignment work repositories. These are work repositories; sync may fetch remotes but must not reset, clean, merge, or switch branches.

Group by assignment kind before the original repo name:

```text
assignments/DSCI_523_lab1_yz2000/ -> DSCI_523/assignments/lab1/DSCI_523_lab1_yz2000/
assignments/DSCI_523_worksheet1_yz2000/ -> DSCI_523/assignments/worksheet1/DSCI_523_worksheet1_yz2000/
assignments/DSCI_521_lab0a_yz2000/ -> DSCI_521/assignments/lab0a/DSCI_521_lab0a_yz2000/
```

The original repository name stays intact because it is the remote identity and easiest debugging handle.

### `projects/`

User-created course projects and demos. Move project directories into the matching course and remove the repeated course code from the project directory name.

Examples:

```text
project/2026-08-31 DSCI 523 self-learning-demo/ -> DSCI_523/projects/2026-08-31 self-learning-demo/
project/2026-09-01 DSCI 523 lec01-readr-dplyr-tidyr/ -> DSCI_523/projects/2026-09-01 lec01-readr-dplyr-tidyr/
```

Project directories move as whole units because notebooks and scripts use cwd-relative paths such as `data/...`.

## Shared Layout

```text
shared/
  resources/
    index.md
    messages_by_courses/
      life
      quiz_and_cheetsheet_details.txt
    mds-2026-27/
      orientation/
      lab-sections/
      student-reps/
    ubc-mds/
      <public repos for inactive or out-of-program courses>/
```

Shared contains material that is not owned by exactly one active course.

Examples:

- `resources/index.md` is a source/channel index for the whole program.
- `orientation/`, `lab-sections/`, and `student-reps/` are program-level current-year repositories.
- `life` and `quiz_and_cheetsheet_details.txt` are not course-owned.
- Public mirrors for future/inactive courses stay here until the course becomes active enough to justify a top-level course directory.

## Admin Layout

```text
admin/
  sources.conf
  sync_course_repos.sh
  cal_filter.py
  block-schedule-prompt.txt
  assignments.txt
```

Admin contains operational tooling, not study material. Moving the sync script under `admin/` requires it to compute the repository root as the parent of the script directory, not the script directory itself.

## Sync Routing Design

`sync_course_repos.sh` must stop treating `dest` as the final clone root for every repository in a source. It needs deterministic routing from repository name to final path.

Required routing behavior:

```text
Current-year course repo:
  repo: DSCI_523_r-prog_students
  mode: mirror
  path: DSCI_523/official/current/DSCI_523_r-prog_students

Public active-course repo:
  repo: DSCI_523_r-prog
  mode: mirror
  path: DSCI_523/official/public/DSCI_523_r-prog

Assignment repo:
  repo: DSCI_523_lab1_yz2000
  mode: work
  path: DSCI_523/assignments/lab1/DSCI_523_lab1_yz2000

Shared current-year repo:
  repo: orientation
  mode: mirror
  path: shared/resources/mds-2026-27/orientation
```

Course code parsing rule:

- Match `^(DSCI|COLX)_[0-9]{3}` at the start of the repository name.
- Convert that prefix directly to the root course directory name, e.g. `DSCI_523`.
- If a repository has no course prefix, route it to `shared/resources/<source-name>/<repo>`.

Assignment kind parsing rule:

- For repositories matching `^(DSCI|COLX)_[0-9]{3}_(.+)_yz2000$`, use the middle capture as the assignment grouping directory.
- Keep the full repo name as the final clone directory.

Active course allowlist for this migration:

```text
DSCI_511
DSCI_521
DSCI_523
DSCI_551
```

If a public mirror has a course prefix outside the active allowlist, route it to `shared/resources/ubc-mds/<repo>` for now.

## `sources.conf` Contract

Keep source discovery in a small manifest, but update its destination semantics so destinations describe source families, not final per-course paths.

Recommended rows:

```text
mds-2026-27 ; https://github.ubc.ca/api/v3 ; mds-2026-27 ;               ; _yz2000$ ; current ; mirror
ubc-mds     ; https://api.github.com       ; UBC-MDS     ; ^(DSCI|COLX)_ ;          ; public  ; mirror
assignments ; https://github.ubc.ca/api/v3 ; mds-2026-27 ; _yz2000$      ;          ; work    ; work
```

`dest` can be renamed to `family` in the script and comments. The file format should stay semicolon-delimited to preserve the existing reason documented in the file.

## `.gitignore` Contract

Do not ignore whole course directories. Ignore only nested cloned repositories and generated local state.

Expected ignore rules:

```gitignore
# Upstream clones and personal assignment repos are nested Git repositories.
DSCI_*/official/current/*/
DSCI_*/official/public/*/
DSCI_*/assignments/*/*/
COLX_*/official/current/*/
COLX_*/official/public/*/
COLX_*/assignments/*/*/
shared/resources/mds-2026-27/*/
shared/resources/ubc-mds/*/

.DS_Store
```

This keeps `DSCI_523/README.md`, `DSCI_523/notes/`, and `DSCI_523/projects/` tracked by the main repository while avoiding accidental tracking of nested clones.

## Path Update Scope

Update tracked text references after moving files:

- `resources/index.md` after it moves to `shared/resources/index.md`;
- every moved `notes/resources.md` path that currently references `resources/mds-2026-27/...`;
- project READMEs with absolute paths under `/Users/youralmight/workspaces/reps/mdscl/project/...`;
- script comments/help text in `admin/sync_course_repos.sh`;
- `.gitignore`;
- `admin/sources.conf` comments.

Do not rewrite paths inside ignored upstream mirror repositories unless needed for their own execution. They are upstream-owned.

## Migration Order

1. Create root course directories for `DSCI_511`, `DSCI_521`, `DSCI_523`, and `DSCI_551`.
2. Move user-authored course notes into `<COURSE>/notes/`.
3. Move DSCI 523 user projects into `DSCI_523/projects/`, preserving each project as a whole directory.
4. Move current-year course mirrors into `<COURSE>/official/current/`.
5. Move public active-course mirrors into `<COURSE>/official/public/`.
6. Move assignment work repositories into `<COURSE>/assignments/<kind>/`.
7. Move program-level resources into `shared/resources/`.
8. Move operational tooling into `admin/` and update root resolution in the sync script.
9. Update `.gitignore` and text references.
10. Verify routing and links.

## Verification

Minimum checks after implementation:

1. Run the sync script in offline mode for each source family and verify it looks for existing clones in their new locations.
2. Run list-only mode and verify discovered assignment/current/public lists still write to tracked manifest paths without recreating old `resources/` or `assignments/` roots.
3. Check that nested Git repositories remain nested and are not staged by the main repository.
4. Search tracked files for stale references to:
   - `my_notes/courses/`
   - `resources/mds-2026-27/`
   - `resources/ubc-mds/`
   - `assignments/DSCI_`
   - `/project/2026-`
5. Open or run the DSCI 523 project commands from their new directories to confirm cwd-relative `data/...` paths still work.
6. Confirm root scanning is cleaner: active course dirs, `shared/`, `admin/`, package/tooling files.

## Open Review Points

These are intentional design choices to review before implementation:

1. Public mirrors for inactive courses stay in `shared/resources/ubc-mds/` during the first migration. If the desired rule is "every course-specific public repo gets a root course directory immediately," this spec should change before planning.
2. The extra `courses/` wrapper is removed. Course directories are top-level siblings of `shared/`, `admin/`, and package files.
3. Assignment directories include a human grouping layer (`lab1`, `worksheet1`) while preserving the original clone directory below it.
4. Official upstream clone directory names are not normalized.
