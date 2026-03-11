from __future__ import annotations

from datetime import datetime
from pathlib import Path

from pytz import timezone

from financial_news_bot.config import Settings
from financial_news_bot.crawler import RSS_SOURCES, fetch_news_from_rss
from financial_news_bot.summarizer import LLMSummarizer


TZ_SHANGHAI = timezone("Asia/Shanghai")



def run_daily_brief(settings: Settings) -> Path:
    news = fetch_news_from_rss(RSS_SOURCES)
    top_news = news[: settings.max_news_items]

    summarizer = LLMSummarizer(
        base_url=settings.llm_base_url,
        api_key=settings.llm_api_key,
        model=settings.llm_model,
    )
    summary = summarizer.summarize(top_news)

    now = datetime.now(TZ_SHANGHAI)
    output = settings.output_dir / now.strftime("%Y-%m-%d.md")
    output.parent.mkdir(parents=True, exist_ok=True)

    with output.open("w", encoding="utf-8") as f:
        f.write(f"# 金融新闻日报 ({now.strftime('%Y-%m-%d %H:%M %Z')})\n\n")
        f.write(f"_Model: {summary.model}_\n\n")
        f.write(summary.markdown)
        f.write("\n\n## 原始新闻\n")
        for item in top_news:
            pub = item.published_at.isoformat() if item.published_at else "unknown"
            f.write(f"- {item.title} ({pub})\n  - {item.link}\n")

    return output
