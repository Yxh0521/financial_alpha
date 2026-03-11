from dataclasses import dataclass
from os import getenv
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    llm_base_url: str
    llm_api_key: str
    llm_model: str
    max_news_items: int
    output_dir: Path



def load_settings() -> Settings:
    return Settings(
        llm_base_url=getenv("LLM_BASE_URL", "https://api.openai.com/v1"),
        llm_api_key=getenv("LLM_API_KEY", ""),
        llm_model=getenv("LLM_MODEL", "gpt-4o-mini"),
        max_news_items=int(getenv("MAX_NEWS_ITEMS", "30")),
        output_dir=Path(getenv("OUTPUT_DIR", "output")),
    )
