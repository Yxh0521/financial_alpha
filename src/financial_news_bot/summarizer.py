from __future__ import annotations

import json
from dataclasses import dataclass
from urllib.request import Request, urlopen

from financial_news_bot.crawler import NewsItem


@dataclass(frozen=True)
class SummaryResult:
    markdown: str
    model: str


class LLMSummarizer:
    def __init__(self, base_url: str, api_key: str, model: str) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.model = model

    def summarize(self, news: list[NewsItem]) -> SummaryResult:
        if not self.api_key:
            raise ValueError("LLM_API_KEY is empty. Please configure environment variables first.")

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "你是一名资深金融分析师，输出中文总结。"},
                {"role": "user", "content": _build_prompt(news)},
            ],
            "temperature": 0.2,
        }

        req = Request(
            url=f"{self.base_url}/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )

        with urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read().decode("utf-8"))

        content = data["choices"][0]["message"]["content"].strip()
        return SummaryResult(markdown=content, model=self.model)



def _build_prompt(news: list[NewsItem]) -> str:
    headline_lines = []
    for idx, item in enumerate(news, start=1):
        ts = item.published_at.isoformat() if item.published_at else "unknown"
        headline_lines.append(f"{idx}. [{item.source}] {item.title} ({ts}) {item.link}")

    joined = "\n".join(headline_lines)
    return (
        "请基于以下金融新闻生成日报，要求：\n"
        "1. 生成《今日金融快报》\n"
        "2. 分为宏观、股市、外汇/大宗商品、风险提示四个部分\n"
        "3. 每个部分3-5条要点\n"
        "4. 最后给出今天值得跟踪的3个关键词\n\n"
        f"新闻列表：\n{joined}"
    )
