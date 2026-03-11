# Financial News Daily Brief (开源版)

一个可以**每日自动抓取金融新闻**、调用**大模型生成中文总结**、并在**北京时间早上 09:00 定时执行**的开源项目。

## 功能

- 多源 RSS 抓取金融新闻（可扩展）
- 自动去重、按发布时间排序
- 调用 OpenAI 兼容接口进行中文总结
- APScheduler 定时任务（Asia/Shanghai 每天 09:00）
- 输出 Markdown 日报文件，便于归档或二次分发

## 快速开始

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
cp .env.example .env
```

编辑 `.env`（或直接配置环境变量）：

- `LLM_BASE_URL`: 大模型 API 地址（OpenAI 兼容）
- `LLM_API_KEY`: API Key
- `LLM_MODEL`: 模型名
- `MAX_NEWS_ITEMS`: 每次参与总结的新闻数量上限
- `OUTPUT_DIR`: 报告输出目录

### 立即执行一次

```bash
export $(cat .env | xargs)
financial-news-bot --once
```

### 启动定时任务（每天北京时间 09:00）

```bash
export $(cat .env | xargs)
financial-news-bot
```

## 项目结构

```text
src/financial_news_bot/
  config.py      # 配置读取
  crawler.py     # RSS 新闻抓取
  summarizer.py  # LLM 总结
  workflow.py    # 抓取 + 总结 + 输出
  scheduler.py   # 定时调度
  main.py        # CLI 入口
```

## 开源建议

- 你可以把 `output/*.md` 接到企业微信机器人、Telegram Bot、邮件系统。
- 如果你希望聚合中文资讯，可补充国内财经媒体 RSS。
- 如果目标是生产可用，建议接入数据库、缓存和失败重试机制。

## License

MIT
