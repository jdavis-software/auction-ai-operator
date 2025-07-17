"""
Light wrapper around APScheduler for cron‑like or interval scheduling.
"""
from apscheduler.schedulers.asyncio import AsyncIOScheduler


def build_scheduler():
    scheduler = AsyncIOScheduler(timezone="UTC")
    scheduler.start()
    return scheduler
