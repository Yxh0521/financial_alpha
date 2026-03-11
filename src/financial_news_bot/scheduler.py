from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from pytz import timezone

from financial_news_bot.config import load_settings
from financial_news_bot.workflow import run_daily_brief



def start_scheduler() -> None:
    tz = timezone("Asia/Shanghai")
    scheduler = BlockingScheduler(timezone=tz)

    scheduler.add_job(
        func=lambda: run_daily_brief(load_settings()),
        trigger=CronTrigger(hour=9, minute=0, timezone=tz),
        id="daily_financial_news_summary",
        replace_existing=True,
    )

    print("Scheduler started: it will run every day at 09:00 Asia/Shanghai")
    scheduler.start()
