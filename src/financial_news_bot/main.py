import argparse

from financial_news_bot.config import load_settings
from financial_news_bot.scheduler import start_scheduler
from financial_news_bot.workflow import run_daily_brief



def run() -> None:
    parser = argparse.ArgumentParser(description="金融新闻自动摘要项目")
    parser.add_argument("--once", action="store_true", help="立即执行一次，不启动定时任务")
    args = parser.parse_args()

    if args.once:
        output = run_daily_brief(load_settings())
        print(f"日报已生成: {output}")
        return

    start_scheduler()


if __name__ == "__main__":
    run()
