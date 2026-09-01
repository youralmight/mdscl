# /// script
# requires-python = ">=3.11"
# ///
"""从源日历筛事件，全量重建到目标日历。

每次跑都是全量重建：先清空目标日历，再把源日历里匹配的事件加进去。
跑两次结果一样。源日历一个字都不动。

正则匹配的对象是每个事件的 "标题 \\t 地点 \\t 描述" 拼成的一行，不含日期、
id、日历名。用 Python 的 re，lookahead / 分组 / (?i) 这些跟 grep -P 一致。

重复事件会被展开成一个个独立事件——gcalcli 读不出 RRULE
（agenda --details 的可选值里根本没有 recurrence），保不住重复规则。

第一次用之前要先授权：uvx --from gcalcli gcalcli init


uv run cal_filter.py \
    --src 'courses' \
    --dst 'courses to attend' \
    --pattern '^DSCI 5(?:11|21) Lab'
"""

import argparse
import csv
import os
import re
import subprocess
from datetime import date

# 默认用装好的 gcalcli，不用 uvx：写入是一个事件一次调用，走 uvx 每次都要重新
# resolve 依赖，几十个事件就是几十次。装法：uv tool install gcalcli
GCALCLI = os.environ.get("GCALCLI", "gcalcli").split()
TIMEOUT = 120


def sync_calendar(*, src, dst, pattern, invert=False, start="1970-01-01",
                  end="2099-12-31", dry_run=False):
    # uv run cal_filter.py --src 'Yi Zhang Calendar (Canvas)' --dst 'My MDS CL courses' --pattern 'DSCI 5(23|51)' --invert --dry-run

    # 读源日历。--tsv 首行是表头，DictReader 按列名取，不依赖列序。
    print(f">>> 读 [{src}] {start} → {end}")
    tsv = subprocess.run(
        [*GCALCLI, "--calendar", src, "agenda", "--tsv", "--details", "all", start, end],
        check=True, timeout=TIMEOUT, text=True, capture_output=True,
    ).stdout
    rows = list(csv.DictReader(tsv.splitlines(), delimiter="\t"))
    print(f"    {len(rows)} 个事件")

    # 筛。事件描述里的换行被 gcalcli 转义成字面的 \n，所以一个事件永远是一行。
    rx = re.compile(pattern)
    matched = [r for r in rows
               if bool(rx.search("\t".join((r["title"], r["location"], r["description"]))))
               is not invert]
    print(f">>> 正则 /{pattern}/{' 反向' if invert else ''} 命中 {len(matched)} / {len(rows)}")

    # 两个"什么都不做"的出口都排在清空之前——清空是唯一不可逆的动作。
    if not matched:
        raise SystemExit("一个都没匹配上，不动目标日历。")
    if dry_run:
        for r in matched:
            print(f"    {r['start_date']} {r['start_time']:5} {r['title']}")
        print(f">>> dry run，目标日历 [{dst}] 未改动。")
        return matched

    # 清空目标日历。gcalcli 没有"清空"操作，delete 必须收一个搜索词：空串它
    # 写死了报错，一个空格是 truthy 能过检查，再原样传给 Google 的 q= 参数。
    print(f">>> 清空 [{dst}]")
    subprocess.run(
        [*GCALCLI, "--calendar", dst, "delete", "--iamaexpert", " ", start, end],
        check=True, timeout=TIMEOUT,
    )

    # 写入。不在这里加 retry：gcalcli 内部对 API 调用已有指数退避，外面再包一层
    # 会在"加成功了但响应丢了"的时候造出重复事件。失败就 raise，重跑整条流程。
    print(f">>> 写入 [{dst}]")
    for i, r in enumerate(matched, 1):
        args = ["--calendar", dst, "add", "--noprompt", "--title", r["title"]]
        if r["location"]:
            args += ["--where", r["location"]]
        if r["description"]:
            args += ["--description", r["description"]]
        if r["start_time"]:
            args += ["--when", f"{r['start_date']} {r['start_time']}",
                     "--end", f"{r['end_date']} {r['end_time']}"]
        else:
            # 全天事件必须用 --duration（天数），不能用 --end：gcalcli 的
            # get_times_from_duration 里 `if end is not None` 会跳过 allday 分支，
            # start 留成 datetime，塞进 Google 只收 YYYY-MM-DD 的 date 字段 → 400。
            # end_date 和 duration 都是排他式，天数直接相减即可。
            days = (date.fromisoformat(r["end_date"]) - date.fromisoformat(r["start_date"])).days
            args += ["--allday", "--when", r["start_date"], "--duration", str(days)]
        subprocess.run([*GCALCLI, *args], check=True, timeout=TIMEOUT,
                       stdout=subprocess.DEVNULL)
        print(f"\r    {i} / {len(matched)}", end="")

    print(f"\n全部成功：{len(matched)} 个事件已重建到 [{dst}]")
    return matched


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--src", required=True, help="源日历名，gcalcli list 里的原文")
    p.add_argument("--dst", required=True, help="目标日历名，必须是 owner 权限")
    p.add_argument("--pattern", required=True, help="正则，匹配 '标题\\t地点\\t描述'")
    p.add_argument("--invert", action="store_true", help="反向：留下不匹配的")
    p.add_argument("--start", default="1970-01-01")
    p.add_argument("--end", default="2099-12-31")
    p.add_argument("--dry-run", action="store_true", help="只打印，不动任何日历")
    sync_calendar(**vars(p.parse_args()))
