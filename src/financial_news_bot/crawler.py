from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from typing import Iterable
import xml.etree.ElementTree as ET
from urllib.request import Request, urlopen

RSS_SOURCES = [
    "https://feeds.a.dj.com/rss/RSSMarketsMain.xml",
    "https://www.investing.com/rss/news_25.rss",
    "https://www.ft.com/?format=rss",
]


@dataclass(frozen=True)
class NewsItem:
    title: str
    link: str
    source: str
    published_at: datetime | None



def fetch_news_from_rss(urls: Iterable[str], timeout: int = 15) -> list[NewsItem]:
    results: list[NewsItem] = []
    seen_links: set[str] = set()

    for url in urls:
        req = Request(url, headers={"User-Agent": "financial-news-bot/0.1"})
        with urlopen(req, timeout=timeout) as resp:
            raw_xml = resp.read().decode("utf-8", errors="ignore")

        root = ET.fromstring(raw_xml)

        for item in root.findall(".//item"):
            title = _get_text(item, "title")
            link = _get_text(item, "link")
            pub_date = _get_text(item, "pubDate")

            if not title or not link or link in seen_links:
                continue

            seen_links.add(link)
            results.append(
                NewsItem(
                    title=title.strip(),
                    link=link.strip(),
                    source=url,
                    published_at=_parse_pub_date(pub_date),
                )
            )

    return sorted(results, key=lambda x: x.published_at or datetime.min.replace(tzinfo=timezone.utc), reverse=True)



def _get_text(node: ET.Element, tag: str) -> str:
    child = node.find(tag)
    return child.text if child is not None and child.text else ""



def _parse_pub_date(raw: str) -> datetime | None:
    if not raw:
        return None
    try:
        dt = parsedate_to_datetime(raw)
        if dt.tzinfo is None:
            return dt.replace(tzinfo=timezone.utc)
        return dt
    except (TypeError, ValueError):
        return None
