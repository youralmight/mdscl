# DSCI 523 Quiz 1 Cheat Sheet — Companion Explanation

**Not intended for upload or exam use.** This companion preserves the source context and editorial decisions excluded from the exam-facing [Cheat Sheet](quiz1-cheatsheet.md). Its source is [Quiz 1 knowledge review](quiz1-knowledge.md).

## Scope and assessment context retained outside the Cheat Sheet

- The knowledge review records Quiz 1 as covering Lecture 1–4, with all non-optional lecture-note content in scope; it records a 30% course weight and a 2026-09-15–18 window.
- It records general MDS quiz logistics: a 50-minute PrairieLearn assessment, a PrairieTest reservation, in-person ORCA completion, check-in/CWL expectations, workspace startup time, package-loading behavior, and automatic grading/submission conventions. These are intentionally not on the Cheat Sheet.
- It marks `str_extract*` and regex capture groups as optional, so they were not carried into the exam artifact.
- The source reports an ambiguity about set operations: a learning objective mentions comparison, while Lecture 4 says they are not tested. They remain absent from the Cheat Sheet rather than being presented as an exam operation.
- The source also records unresolved course-specific conditions about appointment slots/location and whether a Quiz 1 cheat sheet is permitted, supplied, or student-created. Consult current course instructions rather than treating this companion as authorization.

## Compression and inclusion decisions

The Cheat Sheet retains operations that can decide a coding answer or output shape: reader selection and import parameters; dplyr verbs and vectorized logical rules; tidy-data definitions and pivot arguments; R type/structure checks and extraction shapes; `NA` propagation; lubridate parsers and intervals; stringr return shapes and regex escaping; factor ordering; join row/column retention and duplicate-key effects; and base-R branch/loop edge cases.

Narrative motivation, style/process advice, scope evidence, dates, grading and platform instructions, source provenance, and document-reading guidance were removed. Repeated prose was compressed into tables, signatures, return-shape statements, contrast rules, and small runnable examples. The main tradeoff is density: explanations of *why* tidy data, factors, and copy-on-modify matter are shorter, but each retains the practical decision rule or pitfall needed to answer a question.

## Provenance retained outside the exam artifact

The knowledge review cites current-year course material: the DSCI 523 R-program README and learning objectives; lecture notebooks 01–04; the section-001 Lecture 4 skeleton; worksheets 1–4, labs 1–2, and section-002 examples; plus the [MDS Quiz Guidelines](https://ubc-mds.github.io/resources_pages/quiz_guidelines/). The knowledge review is the authoritative local synthesis to inspect when course scope or policy needs reconfirmation.
