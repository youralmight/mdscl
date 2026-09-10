# Weekly deadline audit runbook

Use this runbook to answer: **What deadlines do I have this week, and how do you know none were silently missed?**

The deliverable is a concise deadline table plus an auditable reconciliation against every active course's grading table. Do not claim completeness if an authoritative source is inaccessible or an expected item remains unexplained.

## Fixed scope

- Interpret a week as Monday 00:00 through Sunday 23:59 in `America/Vancouver` unless the user gives another range.
- Report deadlines, not general study advice or tasks without a fixed due time.
- Keep submitted work in the table; show that it is submitted.
- Audit Setup Check, Policy Quiz, and pre-lecture quiz streams for completeness; under the standing user preference, omit their individual deadlines from the first table and disclose the exclusion.
- Do not generate an ICS or modify calendars unless asked.

## Source map

Start from `course-index.md` to identify every active course. For each active course, read `<COURSE>/README.md` and follow its named current grading-table and submission-platform sources. A course missing from the convenience map below must still be audited; discover its sources from its README rather than reusing another course's mapping.

Current Block 1 convenience map:

| Course | Grading-table source | Usual live deadline source |
|---|---|---|
| DSCI 511 | `DSCI_511/official/current/DSCI_511_py-prog_students/README.md`, `Deliverables` | Gradescope; quizzes: PrairieTest + PrairieLearn; CL calendar only if these have no date |
| DSCI 521 | `DSCI_521/official/public/DSCI_521_platforms-dsci/index.qmd`, `Assessments` | Gradescope, PrairieLearn, or Canvas as named by the grading table |
| DSCI 523 | `DSCI_523/official/current/DSCI_523_r-prog_students/README.md`, `Deliverables` | Gradescope; quizzes: PrairieTest + PrairieLearn |
| DSCI 551 | `DSCI_551/official/current/DSCI_551_stat-prob-dsci_students/README.md`, `Deliverables` | Gradescope; quizzes: PrairieTest + PrairieLearn; MDS calendar only if these have no date |

Use each course's `notes/messages.md` only to resolve or document a conflict. Assignment repositories and local checkouts describe the work, not whether a submission item is open.

When browser access is needed, follow the global `AGENTS.md`: attach only to the user's existing Brave process/profile/window, use a task-owned background tab, and pin the session to that exact tab. Never fall back to a new browser, profile, window, or foreground tab. Preserve raw page/API responses under one `tmp/runs/<timestamp>_course-deadlines/logs/` directory.

## Procedure

### 1. Fix the audit range

State the exact Monday–Sunday range and Pacific Time before collecting data. Confirmed deadlines belong in the range when their authoritative due time falls inside it. A structure-derived current-week candidate with no authoritative time remains visible as `本周（截止时间待确认）` with an alarm; never invent a date.

### 2. Build the assessment-stream inventory first

For every active course, transcribe each assessment type, its total count, weight, cadence, and stated weeks. Do this before looking at deadline platforms.

Create one working row per assessment stream:

| Course | Assessment type | Full-course structure | What the current week implies | Submission-platform observation | Match? |
|---|---|---|---|---|---|

The inventory must account for every grading-table category, but it should not expand every numbered future item into a user-facing status ledger. Its purpose is to show why the current week does—or does not—create a candidate to check.

### 3. Derive candidates; do not invent dates

Use course structure to detect likely omissions:

- four labs across four teaching weeks means actively check for the current week's lab;
- eight worksheets across four weeks usually means actively check for two that week;
- an assessment explicitly labelled Week 1/2/3/4 must be checked in that week;
- oral checks, quizzes, milestones, surveys, and group work follow stated timing rather than a generic weekly assumption;
- a small count such as two quizzes does not imply even spacing—check the authoritative quiz schedule.

These rules create **candidates to investigate**, never dates. The live source supplies dates. If the structure says an item should be due but the submission platform has no item, treat that mismatch as an alarm, not as proof that nothing is due.

### 4. Check only the relevant live source

For each candidate, open the designated submission platform and record:

- exact title;
- due date and time, including timezone;
- whether the submission item exists and accepts submissions;
- submitted/unsubmitted state where visible;
- source URL and check time.

For each quiz-bearing course, also check PrairieTest for the exam window and reservation state, and PrairieLearn for cheatsheet or practice deadlines. A quiz is not covered merely because its grading-table row was noticed.

Do not browse every platform for every course. Escalate to the syllabus, course message, or calendar only when the designated live source lacks a date or conflicts with another source.

### 5. Compare expectation with submission-platform reality

- Use the current live submission-platform deadline when it conflicts with a syllabus or announcement.
- Report both values and the chosen source under `Problems`; never silently overwrite a conflict.
- Keep submitted work in the deadline table when its deadline falls inside the range.
- **Open/released** means the designated submission platform has created the item and accepts submissions.
- A GitHub assignment repository does not establish that an item is open for submission.
- Do not show repository presence or local checkout/sync state in normal deadline output. Use them only as background diagnostics after an expectation/platform mismatch.
- If course structure or a current syllabus says an item should be due this week but the submission platform has no item, keep it in the deadline table and mark the missing submission item as an alarm.

### 6. Reconcile each assessment stream

For every grading-table stream, answer four questions:

1. What is the full-course count, weight, cadence, or stated week?
2. Does that structure imply a deadline candidate in the audited week?
3. What does the authoritative submission or quiz platform show?
4. Do expectation and platform reality match?

Investigate every mismatch. Also flag:

- four labs/four weeks but no current-week lab on the submission platform;
- eight worksheets/four weeks but fewer than two current-week items without explanation;
- an item due this week whose submission platform has no submission entry;
- a live submission item absent from the grading inventory;
- a quiz-bearing course whose PrairieTest window, reservation state, or relevant PrairieLearn deadline was not checked;
- an unusual time such as `18:01`;
- a submitted in-scope item dropped from the deadline table.

Do not substitute an opaque expected/found/listed count for these rows. The user must be able to see the reasoning for each assessment stream.

## Required report

Use the `mdscl-coursework` skill's `references/weekly-deadline-report-example.md` when available. It defines presentation shape only; never reuse its dates or status.

### 1. This week's deadlines

Sort by deadline, then course and item. State that all times are Pacific Time.

| 时间 | 课程 | 项目 | 提交平台状态 |
|---|---|---|---|

Use concise states:

- `✅ Gradescope 已开放；📤 未提交`
- `✅ PrairieLearn 已开放；📤 已提交`
- `🚨 Syllabus 确认本周 due；Gradescope 没有提交项`
- `🚨 本周（截止时间待确认）；提交平台没有对应项`

“已开放” always means the designated submission platform accepts submissions. Do not mention GitHub or local sync.

### 2. Immediately after this week

Include this short table only when an item just outside Sunday requires action now, such as a Monday cheatsheet deadline or an unbooked exam window.

### 3. Course structure and current-week checks

Use one row per assessment stream:

| 课程 | 评分类型 | 全期结构 | Current-week 核查 |
|---|---|---|---|

Inside the final column, use short line-separated entries:

- `🔎` why the course structure creates—or does not create—a candidate;
- `✅` expected submission item and live due time found;
- `📤` submitted/unsubmitted;
- `🚨` expectation and platform state disagree;
- `⏭️` no graded deadline expected this week.

Quizzes use the same table and reasoning as labs, worksheets, milestones, and other assessment streams. Do not create a quiz-special report section.

### 4. Problems and evidence

`Problems` contains only expectation/platform mismatches, conflicting dates, inaccessible required sources, and immediate risks. Evidence lists source URLs/log paths and check time.

End with a qualified conclusion:

- **Verified:** every grading stream has a visible reasoning row; every current-week candidate is accounted for; every non-excluded candidate appears in the deadline table; excluded streams remain in the assessment-stream reconciliation and the exclusion is disclosed; all expectation/platform comparisons are explained; and every required source was accessible.
- **Not fully verified:** name the exact missing source or unexplained candidate.

## Final checklist

- [ ] Exact week and timezone stated
- [ ] Active courses taken from `course-index.md`
- [ ] Every grading-table assessment stream represented once
- [ ] Count/cadence/stated weeks used to derive current-week candidates
- [ ] Every candidate checked on its designated submission platform
- [ ] Quiz windows, reservations, and relevant PrairieLearn deadlines checked
- [ ] “Open/released” refers only to a submission item that accepts submissions
- [ ] Every in-scope row shows submitted/unsubmitted where visible
- [ ] Expectation/platform mismatches use an alarm and are investigated
- [ ] Repository/local-sync state omitted from normal report output
- [ ] User exclusions applied and disclosed
- [ ] Raw evidence and verification report saved
