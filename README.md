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

Render Markdown directly to a compact US Letter PDF. One-page documents also get a PNG:

```bash
uv run mdscl-cheatsheet DSCI_511/notes/quiz1-cheatsheet.md tmp/quiz1-cheatsheet
```

The renderer tries layouts between two and four columns at 8–10 pt. If none fits one page, it writes the layout with the fewest pages rather than shrinking below 8 pt or truncating content. Standard output always includes `PDF pages: N`; PNG output is limited to one-page documents.
