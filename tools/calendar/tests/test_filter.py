import unittest

from calendar_io import apply_plan
from plan import plan_events


def row(title="keep", start_date="2026-10-05", start_time="", end_date="2026-10-07", end_time=""):
    return {"title": title, "location": "", "description": "", "start_date": start_date,
            "start_time": start_time, "end_date": end_date, "end_time": end_time}


class CalendarPlanTests(unittest.TestCase):
    def test_empty_and_invalid_plans_cannot_delete(self):
        empty = plan_events([], src="s", dst="d", pattern=".")
        calls = []
        with self.assertRaises(ValueError):
            apply_plan(["fake"], empty, runner=lambda *a, **k: calls.append(a))
        self.assertEqual(calls, [])
        with self.assertRaises(ValueError):
            plan_events([row(start_date="bad")], src="s", dst="d", pattern=".")

    def test_timed_dates_and_order_fail_before_apply(self):
        for event in [
            row(start_date="bad", start_time="14:00", end_time="15:00"),
            row(start_time="14:00", end_date="2026-10-05", end_time="13:00"),
            row(start_date="2026-10-07", start_time="14:00", end_date="2026-10-05", end_time="15:00"),
        ]:
            with self.subTest(event=event), self.assertRaises(ValueError):
                plan_events([event], src="s", dst="d", pattern=".")

    def test_empty_or_reversed_replacement_range_is_rejected(self):
        for end in ["2026-10-05", "2026-10-04"]:
            with self.subTest(end=end), self.assertRaises(ValueError):
                plan_events([row()], src="s", dst="d", pattern=".", start="2026-10-05", end=end)

    def test_regex_and_invert(self):
        rows = [row("alpha"), row("beta")]
        self.assertEqual([e.title for e in plan_events(rows, src="s", dst="d", pattern="^a").events], ["alpha"])
        self.assertEqual([e.title for e in plan_events(rows, src="s", dst="d", pattern="^a", invert=True).events], ["beta"])

    def test_all_day_exclusive_end_duration(self):
        plan = plan_events([row()], src="s", dst="d", pattern=".")
        calls = []
        apply_plan(["fake"], plan, runner=lambda args, **kw: calls.append((args, kw)))
        added = calls[1][0]
        self.assertIn("--allday", added)
        self.assertEqual(added[added.index("--duration") + 1], "2")
        self.assertEqual(added[added.index("--when") + 1], "2026-10-05")

    def test_add_failure_follows_single_delete_without_rollback(self):
        plan = plan_events([row()], src="s", dst="d", pattern=".")
        calls = []
        def fail_add(args, **kwargs):
            calls.append(args)
            if "add" in args:
                raise RuntimeError("add failed")
        with self.assertRaisesRegex(RuntimeError, "add failed"):
            apply_plan(["fake"], plan, runner=fail_add)
        self.assertEqual(len(calls), 2)
        self.assertIn("delete", calls[0])
        self.assertIn("add", calls[1])


if __name__ == "__main__":
    unittest.main()
