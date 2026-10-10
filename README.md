# MDS-CL workspace

Top level is course-first. Open a `DSCI_*` directory for daily study.

## Course directories

- `DSCI_511/` — Programming for Data Science
- `DSCI_521/` — Computing Platforms for Data Science
- `DSCI_523/` — Programming for Data Manipulation
- `DSCI_551/` — Descriptive Statistics and Probability
- `DSCI_512/` — Algorithms and Data Structures
- `DSCI_531/` — Data Visualization I
- `DSCI_552/` — Statistical Inference and Computation I
- `DSCI_571/` — Supervised Learning I
- `course-index.md` — all-year course table

## My MDS-CL course references (2026–27)

- **Personal blog:** [youralmight.github.io](https://youralmight.github.io/) · [GitHub Pages repository](https://github.com/youralmight/youralmight.github.io)

### Official lab roster

| Block | Lab roster | Lecture section | Roster group |
|---|---|---:|---:|
| 1 | **L03** | 2 | **28** |
| 2 | **L04** | 2 | **32** |

Roster source rows identify Justice Zhang: [Block 1 CSV](https://github.ubc.ca/mds-2026-27/lab-sections/blob/main/lab_section_block1_2026-27.csv) · [Block 2 CSV](https://github.ubc.ca/mds-2026-27/lab-sections/blob/main/lab_section_block2_2026-27.csv). The `group_num` is the roster-assigned cohort group; it is distinct from a course project team.

### Block 2 meeting and lab sections

Official source: [UBC MDS Calendar](https://ubc-mds.github.io/calendar/), read by date for Lab L04; the [dated L04 ICS](block2-l04-2026-10-05_2026-11-06.ics) records each actual meeting. All times are Vancouver time.

| Course | Lecture | Assigned lab |
|---|---|---|
| DSCI 531 | Tue/Thu 08:00–09:20, DMP 110 | Thu 14:00–15:50, MCLD 3018, L04 |
| DSCI 552 | Tue/Thu 09:30–10:50, DMP 110 | Tue 14:00–15:50, SPPH B151, L04 |
| DSCI 571 | Mon/Wed 09:30–10:50, SHRM B1009 | Wed 14:00–15:50, MCLD 3018, L04 |
| DSCI 512 | Mon/Wed 12:30–14:00, EOS 135, CL Section 003 | Thu 12:00–14:00, ORCH 3018, CL Lab L05 |

The CL-only DSCI 512 times are separately documented in the [CL course README](https://github.ubc.ca/MDS-CL-2026-27/DSCI_512_alg-data-struct_students/blob/master/README.md) and [CL Canvas Calendar](https://canvas.ubc.ca/courses/204677/pages/course-calendar); the shared MDS L04 calendar's 512-L04 events are not Justice's CL lab. The ICS and each dated event are verified in [`tmp/runs/20261005-144830_l04-calendar-root-readme/agent_report.md`](tmp/runs/20261005-144830_l04-calendar-root-readme/agent_report.md).

### DSCI 521 Block 1 group lab

For the Week 3 collaborative slide-deck lab, Justice was assigned **Group 28**. Sources: [Block 1 roster CSV](https://github.ubc.ca/mds-2026-27/lab-sections/blob/main/lab_section_block1_2026-27.csv), [Group 28 source repository](https://github.ubc.ca/mds-2026-27/DSCI_521_lab3-group_group28), [published Group 28 slides](https://pages.github.ubc.ca/mds-2026-27/DSCI_521_lab3-group_group28/), and [Justice's Gradescope group submission](https://www.gradescope.ca/courses/39412/assignments/208934/submissions/11777779). Block 2 roster group 32 is not this Block 1 project team.

### Personal lab assignment repositories

The following are Justice's per-assignment GitHub repositories, as inventoried by [`tools/repository-sync/work.txt`](tools/repository-sync/work.txt); they are separate from the lab-section/group roster.

| Course | Current personal lab repositories |
|---|---|
| DSCI 511 | [`lab1–lab4`, `worksheet1–worksheet8`](https://github.ubc.ca/mds-2026-27/DSCI_511_py-prog_students) |
| DSCI 521 | [`lab0a`](https://github.ubc.ca/mds-2026-27/DSCI_521_lab0a_yz2000), [`lab0b`](https://github.ubc.ca/mds-2026-27/DSCI_521_lab0b_yz2000); group lab above |
| DSCI 523 | [`lab1–lab4`, `worksheet1–worksheet8`](https://github.ubc.ca/mds-2026-27/DSCI_523_r-prog_students) |
| DSCI 551 | [`lab1–lab4`](https://github.ubc.ca/mds-2026-27/DSCI_551_stat-prob-dsci_students) |
| DSCI 512 | [CL `lab1`](https://github.ubc.ca/MDS-CL-2026-27/DSCI_512_lab1_yz2000) |
| DSCI 531 | [Python `lab1`](https://github.ubc.ca/mds-2026-27/DSCI_531_lab1-py_yz2000) |
| DSCI 552 | [`lab1`](https://github.ubc.ca/mds-2026-27/DSCI_552_lab1_yz2000) |
| DSCI 571 | [`lab1`](https://github.ubc.ca/mds-2026-27/DSCI_571_lab1_yz2000) |


## Directory rules

- Course-specific notes, messages, official material, assignments, and projects live in the course directory.
- `tools/` contains independent repository-sync, calendar, and cheatsheet capabilities; each owns its implementation, inputs, tests, and usage constraints.
- Course repositories go directly into `<COURSE>/official/current/`; syncing a newly released course creates its course directory. Non-course repositories are skipped.

## Sources

- Canvas: https://canvas.ubc.ca/

- Current-year GitHub Enterprise orgs: https://github.ubc.ca/MDS-2026-27 and https://github.ubc.ca/MDS-CL-2026-27. DSCI 512 uses the CL organization, not the V organization's same-named repository.
- Public UBC-MDS org: https://github.com/UBC-MDS — only explicitly retained `official/public/` mirrors are updated; absent historical repositories are not downloaded again.
- MDS-CL project site: https://ubc-mdscl.github.io/
- CL calendar: https://ling.air.arts.ubc.ca/mds-cl-calendar/

## Tools and course workflows

| Capability | Entry from the workspace root | Owned instructions |
|---|---|---|
| Repository synchronization | `uv run --project ../uv_base python tools/repository-sync/sync.py` | [repository-sync](tools/repository-sync/README.md) |
| Calendar filtering/publishing | `uv run --project ../uv_base python tools/calendar/filter.py --help` | [calendar](tools/calendar/README.md) |
| Cheat-sheet rendering | `uv run --project tools/cheatsheet mdscl-cheatsheet SOURCE STEM` | [cheatsheet](tools/cheatsheet/README.md) |

The root `pyproject.toml` is the coursework environment, not a tool package. Renderer dependencies and its lockfile belong to `tools/cheatsheet/`. Sync manifests/configuration belong to `tools/repository-sync/`; the three tools do not call each other.

Deadline auditing and quiz knowledge/content-selection workflows belong to the installed `mdscl-coursework` skill and its references. Current course state belongs to the course directories and `course-index.md`, not a duplicated Block-specific table in tool documentation.

## Saved links

- UBC/Vancouver food map: https://maps.app.goo.gl/8w3j6JqDAKRPJhvV6
- UBC/Vancouver activity map: https://maps.app.goo.gl/DzbCrP6MsNguaRjh8
- Quiz cheatsheet guidance: https://ubc-mds.github.io/resources_pages/quiz/#creating-a-cheatsheet

