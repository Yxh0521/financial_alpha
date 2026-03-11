from datetime import datetime, timezone

from financial_news_bot.crawler import NewsItem
from financial_news_bot.summarizer import _build_prompt



def test_build_prompt_contains_news_lines() -> None:
    items = [
        NewsItem(
            title="Fed keeps rates unchanged",
            link="https://example.com/fed",
            source="rss://demo",
            published_at=datetime(2025, 1, 1, tzinfo=timezone.utc),
        )
    ]

    prompt = _build_prompt(items)

    assert "今日金融快报" in prompt
    assert "Fed keeps rates unchanged" in prompt
    assert "https://example.com/fed" in prompt
