"""Pure event selection and validation for calendar replacement."""
from dataclasses import dataclass
from datetime import date, datetime
import re
from typing import Mapping, Sequence


@dataclass(frozen=True)
class Event:
    title: str
    location: str
    description: str
    start_date: str
    start_time: str
    end_date: str
    end_time: str
    all_day_days: int = 0



@dataclass(frozen=True)
class Plan:
    src: str
    dst: str
    start: str
    end: str
    pattern: str
    invert: bool
    events: tuple[Event, ...]


def plan_events(rows: Sequence[Mapping[str, str]], *, src: str, dst: str,
                pattern: str, invert: bool = False, start: str = "1970-01-01",
                end: str = "2099-12-31") -> Plan:
    first_day = date.fromisoformat(start)
    last_day = date.fromisoformat(end)
    if last_day <= first_day:
        raise ValueError(f"invalid replacement range: {start} through {end}")
    rx = re.compile(pattern)
    selected = []
    for row in rows:
        if bool(rx.search("\t".join((row["title"], row["location"], row["description"])))) == invert:
            continue
        first = date.fromisoformat(row["start_date"])
        last = date.fromisoformat(row["end_date"])
        days = 0
        if row["start_time"]:
            starts_at = datetime.combine(first, datetime.strptime(row["start_time"], "%H:%M").time())
            ends_at = datetime.combine(last, datetime.strptime(row["end_time"], "%H:%M").time())
            if ends_at <= starts_at:
                raise ValueError(f"invalid timed event range: {starts_at} through {ends_at}")
        else:
            if row["end_time"] or last <= first:
                raise ValueError(f"invalid all-day event range: {first} through {last}")
            days = (last - first).days
        selected.append(Event(row["title"], row["location"], row["description"],
                              row["start_date"], row["start_time"], row["end_date"],
                              row["end_time"], days))
    return Plan(src, dst, start, end, pattern, invert, tuple(selected))
