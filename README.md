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
- No shared bucket. If material belongs to a course, put it there; otherwise keep it in `admin/` or this README.

## Sources

- Canvas: https://canvas.ubc.ca/
- Current-year GitHub Enterprise org: https://github.ubc.ca/MDS-2026-27
- Public historical UBC-MDS org: https://github.com/UBC-MDS
- MDS-CL project site: https://ubc-mdscl.github.io/
- CL calendar: https://ling.air.arts.ubc.ca/mds-cl-calendar/

Weekly deadline audits: follow [`admin/deadline-audit-runbook.md`](admin/deadline-audit-runbook.md).

Use `admin/sync_course_repos.sh` with `admin/sources.conf` to update upstream clones.

## Saved links

- UBC/Vancouver food map: https://maps.app.goo.gl/8w3j6JqDAKRPJhvV6
- UBC/Vancouver activity map: https://maps.app.goo.gl/DzbCrP6MsNguaRjh8
- Quiz cheatsheet guidance: https://ubc-mds.github.io/resources_pages/quiz/#creating-a-cheatsheet

## Render a Quiz Cheat Sheet

Install the macOS native text-layout library once, then sync the project:

```bash
brew install pango
uv sync
```

Render Markdown directly to compact US Letter HTML, PDF, and PNG:

```bash
uv run mdscl-cheatsheet DSCI_511/notes/quiz1-cheatsheet.md tmp/quiz1-cheatsheet
```

Body text defaults to 8 pt; use `--font-size 9` or `--font-size 10` to override it.

The renderer has no math engine, so cheat-sheet source must not contain LaTeX math markup: `$...$`, `$$...$$`, `\(...\)` and `\[...\]` are rejected with an error (write formulas as plain text instead, e.g. `P(Aᶜ) = 1 − P(A)`). See [`admin/quiz-cheatsheet-workflow.md`](admin/quiz-cheatsheet-workflow.md).

At the chosen size, the renderer compares two-, three-, and four-column layouts. It selects the fewest pages, breaking ties in favor of fewer columns. It saves a styled `.html`, a complete `.pdf`, and one PNG per PDF page. A one-page Cheat Sheet uses `<output-stem>.png`; multipage output uses `<output-stem>-page-1.png`, `<output-stem>-page-2.png`, and so on. Standard output always includes `PDF pages: N`.
