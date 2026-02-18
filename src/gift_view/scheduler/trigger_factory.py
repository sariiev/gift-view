from datetime import datetime, timedelta, timezone

from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger


def build_trigger(interval: int) -> CronTrigger | IntervalTrigger:
    if interval in (60, 180, 300, 900, 1800):
        return CronTrigger(
            minute=f"*/{interval // 60}",
            second=0,
            timezone=timezone.utc
        )

    if interval in (3600, 7200, 14400, 21600, 28800, 43200):
        return CronTrigger(
            hour=f"*/{interval // 3600}",
            minute=0,
            second=0,
            timezone=timezone.utc
        )

    if interval == 86400:
        return CronTrigger(
            hour=0,
            minute=0,
            second=0,
            timezone=timezone.utc
        )

    now = datetime.now(tz=timezone.utc)
    next_run = now.replace(microsecond=0) + timedelta(seconds=interval)

    return IntervalTrigger(
        seconds=interval,
        start_date=next_run,
        timezone=timezone.utc
    )