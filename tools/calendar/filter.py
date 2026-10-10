#!/usr/bin/env python3
"""Select events from a source calendar and replace a bounded target range."""
import argparse
import os

from calendar_io import apply_plan, read_events
from plan import plan_events


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--src", required=True, help="source calendar name")
    parser.add_argument("--dst", required=True, help="destination calendar name")
    parser.add_argument("--pattern", required=True, help="regex over title, location, description")
    parser.add_argument("--invert", action="store_true", help="select nonmatching events")
    parser.add_argument("--start", default="1970-01-01")
    parser.add_argument("--end", default="2099-12-31")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    command = tuple(os.environ.get("GCALCLI", "gcalcli").split())
    print(f">>> 读 [{args.src}] {args.start} → {args.end}")
    rows = read_events(command, args.src, args.start, args.end)
    print(f"    {len(rows)} 个事件")
    plan = plan_events(rows, src=args.src, dst=args.dst, pattern=args.pattern,
                       invert=args.invert, start=args.start, end=args.end)
    print(f">>> 正则 /{args.pattern}/{' 反向' if args.invert else ''} 命中 {len(plan.events)} / {len(rows)}")
    if not plan.events:
        parser.exit(1, "一个都没匹配上，不动目标日历。\n")
    if args.dry_run:
        for event in plan.events:
            print(f"    {event.start_date} {event.start_time:5} {event.title}")
        print(f">>> dry run，目标日历 [{plan.dst}] 未改动。")
        return plan
    print(f">>> 清空 [{plan.dst}]，再写入 {len(plan.events)} 个事件")
    apply_plan(command, plan)
    print(f"全部成功：{len(plan.events)} 个事件已重建到 [{plan.dst}]")
    return plan


if __name__ == "__main__":
    main()
