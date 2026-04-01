import json
from datetime import datetime
from pathlib import Path

from app.api_clients.news_api import get_news

NEWS_CACHE = Path("data/news.json")


def update_news() -> dict:
    """Fetch and store filtered news locally."""
    raw = get_news()

    if "error" in raw:
        return raw

    articles = raw.get("articles", [])

    # Keep only key fields (clean + lightweight)
    cleaned = []
    for article in articles:
        cleaned.append({
            "title": article.get("title"),
            "description": article.get("description"),
            "url": article.get("url"),
            "source": article.get("source", {}).get("name"),
            "published_at": article.get("publishedAt")
        })

    result = {
        "timestamp": datetime.utcnow().isoformat(),
        "articles": cleaned
    }

    # Save locally
    NEWS_CACHE.parent.mkdir(exist_ok=True)
    with open(NEWS_CACHE, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    return result


def load_news() -> dict:
    """Load cached news."""
    if not NEWS_CACHE.exists():
        return {}

    with open(NEWS_CACHE, "r", encoding="utf-8") as f:
        return json.load(f)
