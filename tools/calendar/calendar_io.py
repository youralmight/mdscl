"""Deterministic subprocess boundary for gcalcli calendar I/O."""
import csv
import io
import subprocess
from typing import Callable, Sequence

from plan import Plan

TIMEOUT = 120




def read_events(command: Sequence[str], src: str, start: str, end: str,
                runner: Callable = subprocess.run) -> list[dict[str, str]]:
    result = runner([*command, "--calendar", src, "agenda", "--tsv", "--details", "all", start, end],
                    check=True, timeout=TIMEOUT, text=True, capture_output=True)
    return list(csv.DictReader(io.StringIO(result.stdout), delimiter="\t"))




def apply_plan(command: Sequence[str], plan: Plan,
               runner: Callable = subprocess.run) -> None:
    if not plan.events:
        raise ValueError("refusing to apply an empty calendar plan")
    runner([*command, "--calendar", plan.dst, "delete", "--iamaexpert", " ", plan.start, plan.end],
           check=True, timeout=TIMEOUT)
    # Delete then add is intentionally nontransactional: an add failure leaves the
    # destination partially rebuilt. No retries or rollback are attempted.
    for event in plan.events:
        args = [*command, "--calendar", plan.dst, "add", "--noprompt", "--title", event.title]
        if event.location:
            args += ["--where", event.location]
        if event.description:
            args += ["--description", event.description]
        if event.start_time:
            args += ["--when", f"{event.start_date} {event.start_time}",
                     "--end", f"{event.end_date} {event.end_time}"]
        else:
            args += ["--allday", "--when", event.start_date, "--duration", str(event.all_day_days)]
        runner(args, check=True, timeout=TIMEOUT, stdout=subprocess.DEVNULL)
