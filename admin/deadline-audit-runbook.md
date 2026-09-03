# Weekly deadline audit runbook

Use this runbook to answer: **What deadlines do I have this week, and how do you know none were silently missed?**

The deliverable is a concise deadline table plus an auditable reconciliation against every active course's grading table. Do not claim completeness if an authoritative source is inaccessible or an expected item remains unexplained.

## Fixed scope

- Interpret a week as Monday 00:00 through Sunday 23:59 in `America/Vancouver` unless the user gives another range.
- Report deadlines, not general study advice or tasks without a fixed due time.
- Keep submitted work in the table; show that it is submitted.
- Exclude Setup Check, Policy Quiz, and pre-lecture quizzes unless the user explicitly changes this preference.
- Do not generate an ICS or modify calendars unless asked.

## Source map

Start from local files; open only the live platform needed for a candidate deadline.

| Course | Grading-table source | Usual live deadline source |
|---|---|---|
| DSCI 511 | `DSCI_511/official/current/DSCI_511_py-prog_students/README.md`, `Deliverables` | Gradescope; CL calendar only if Gradescope has no date |
| DSCI 521 | `DSCI_521/official/public/DSCI_521_platforms-dsci/index.qmd`, `Assessments` | Gradescope, PrairieLearn, or Canvas as named by the grading table |
| DSCI 523 | `DSCI_523/official/current/DSCI_523_r-prog_students/README.md`, `Deliverables` | Gradescope |
| DSCI 551 | `DSCI_551/official/current/DSCI_551_stat-prob-dsci_students/README.md`, `Deliverables` | Gradescope; CL calendar only if Gradescope has no date |

Use `course-index.md` to identify active courses and to cross-check assessment counts and weights. Use each course's `notes/messages.md` only to resolve or document a conflict. Use `assignments/` to check whether a released assignment exists locally; it is not deadline authority.

When browser access is needed, follow the global `AGENTS.md`: attach only to the user's existing Brave process/profile/window, use a task-owned background tab, and pin the session to that exact tab. Never fall back to a new browser, profile, window, or foreground tab. Preserve raw page/API responses under one `tmp/runs/<timestamp>_course-deadlines/logs/` directory.

## Procedure

### 1. Fix the audit range

State the exact Monday–Sunday range and Pacific Time before collecting data. A deadline is in scope only if its current authoritative due time falls inside that range.

### 2. Build the grading inventory first

For every active course, transcribe every graded category, total count, weight, and any stated week or cadence. Do this before looking at deadline platforms.

Create a working coverage matrix:

| Course | Grading-table requirement | Total count/weight | Expected this week and why | Live evidence | Disposition |
|---|---|---|---|---|---|

Every grading-table row must end in exactly one disposition:

1. `included` — deadline falls in the audited week;
2. `outside week` — current deadline is before or after the range;
3. `excluded by user`;
4. `not released / no date`;
5. `conflict` — sources disagree and need an explicit decision;
6. `unverified` — the required source could not be accessed.

No blank disposition is allowed.

### 3. Derive candidates; do not invent dates

Use course structure to detect likely omissions:

- four labs across four teaching weeks means actively check for that week's lab;
- eight worksheets across four weeks usually means actively check for two that week;
- an assessment explicitly labelled Week 1/2/3/4 must be checked in that week;
- oral checks, quizzes, milestones, surveys, and group work follow their stated week, not a generic weekly assumption.

These rules create **candidates to investigate**, never dates to report. A plausible candidate without authoritative timing is `not released / no date` or `unverified`, not a guessed deadline.

### 4. Check only the relevant live source

For each candidate, open the submission platform named by the grading table. Record:

- exact title;
- due date and time, including timezone;
- released/unreleased state;
- submitted/unsubmitted state where visible;
- source URL and check time.

Do not browse every platform for every course. Escalate to the syllabus, course message, or calendar only when the named live source lacks a date or conflicts with another source.

### 5. Reconcile conflicts and local availability

- Use the current live submission-platform deadline for the main table when it conflicts with a syllabus or announcement.
- Report both values and the chosen source under `Problems`; never silently overwrite a conflict.
- A submitted assignment remains in the deadline table.
- A live released assignment missing from the local `assignments/` directory remains in the table and is flagged `本地未找到作业`.
- A known in-scope deadline for an unreleased item remains in the table with status `未发布`.

### 6. Run completeness and plausibility checks

For each course, verify both set equalities:

`grading inventory = included ∪ outside week ∪ excluded ∪ not released/no date ∪ conflicts ∪ unverified`

`expected in-week candidates = final table ∪ unresolved difference`

The disposition sets must not overlap. A verified report requires an empty unresolved difference.

Then report:

| Course | Expected this week | Found on authoritative sources | Listed in final table | Unresolved difference |
|---|---:|---:|---:|---:|

Investigate any non-zero difference. Also flag:

- four labs/four weeks but no lab candidate for a teaching week;
- eight worksheets/four weeks but fewer than two candidates without explanation;
- a live released item absent from the grading inventory;
- a grading item absent from every release/deadline source;
- an unusual time such as `18:01`;
- a deadline outside the stated week appearing in the final table;
- duplicate rows or an item dropped because it was submitted.

## Required report

### Deadline table

Sort by deadline, then course and assignment name. State that all times are Pacific Time.

| 时间 | 课程 | 作业名字 | 发布状态 |
|---|---|---|---|

Use concise statuses such as:

- `已发布；未提交`
- `已发布；已提交`
- `已发布；本地未找到作业；未提交`
- `未发布`
- `无法核实`

### Coverage proof

After the deadline table, provide:

1. the completed grading-table coverage matrix;
2. the per-course count table showing expected, found, listed, and difference;
3. a `Problems` list covering every conflict, inaccessible source, missing local assignment, and unexplained candidate;
4. an evidence list with source URLs/log paths and the check time.

End with one of these conclusions:

- **Verified:** every grading item has a disposition, every expected in-week item appears in the deadline table, all count differences are zero, and no source required for the conclusion was inaccessible.
- **Not fully verified:** name the exact missing source or unexplained item. Do not say the table is complete.

## Final checklist

- [ ] Exact week and timezone stated
- [ ] Active courses taken from `course-index.md`
- [ ] Every grading-table category has one disposition
- [ ] Weekly cadence used to probe for missing items
- [ ] Every final row has live or explicitly qualified authoritative evidence
- [ ] Submitted work retained
- [ ] User exclusions applied and disclosed
- [ ] Source conflicts and missing local assignments reported
- [ ] Per-course expected/found/listed counts reconcile
- [ ] Raw evidence and verification report saved
