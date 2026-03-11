from financial_news_bot.crawler import _parse_pub_date



def test_parse_pub_date_invalid_returns_none() -> None:
    assert _parse_pub_date("not-a-date") is None
