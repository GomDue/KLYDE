import json
from datetime import datetime
from dateutil import parser as date_parser
from models.news import NewsArticle

def to_record(raw: str) -> NewsArticle:
    news_json = json.loads(raw)

    link = news_json.get("link")
    title = news_json.get("title")
    if not link or not title:
        raise ValueError("missing link/title")

    published = news_json.get("published") or ""
    try:
        dt = date_parser.parse(published)
    except Exception:
        dt = datetime.now()

    news = NewsArticle(
        title=title,
        writer=news_json.get("author") or "unknown",
        write_dt=dt,
        content=news_json.get("content") or (news_json.get("description") or ""),
        category=news_json.get("category") or "미분류",
        url=link,
        source=news_json.get("source") or "unknown",
        keywords=news_json.get("keywords") or [],
    )
    return news
