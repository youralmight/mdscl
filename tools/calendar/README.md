# Calendar filter

Run from the repository root with `uv run --project ../uv_base python tools/calendar/filter.py --src SOURCE --dst TARGET --pattern REGEX [--invert] [--start YYYY-MM-DD] [--end YYYY-MM-DD] [--dry-run]`. `GCALCLI` optionally supplies the gcalcli executable command (default `gcalcli`). First authorize gcalcli with `uvx --from gcalcli gcalcli init`.

The source is read-only. A non-empty, prevalidated plan clears **all target events** in the requested destination date range and then adds the selected source events. Empty or invalid plans are rejected before deletion; `--dry-run` only reads and prints. Recurring events are expanded by gcalcli into individual events, not recreated as recurrence rules. All-day end dates are exclusive and their duration is computed in the plan. Real apply remains nontransactional: an add failure can leave a partial rebuild. There is no retry or rollback.

Boundaries: `filter.py` owns CLI orchestration, `plan.py` is pure event selection/validation, and `calendar_io.py` owns gcalcli processes. Behavioral checks: `PYTHONPATH=tools/calendar uv run --project ../uv_base python -m unittest discover -s tools/calendar/tests`.
