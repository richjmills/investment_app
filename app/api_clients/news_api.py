import requests

from app.config import NEWS_API_KEY

BASE_URL = "https://gnews.io/api/v4/search"


def get_news(query: str = "economy OR inflation OR interest rates OR markets", max_results: int = 10) -> dict:
    """Fetch news articles from GNews."""
    params = {
        "q": query,
        "lang": "en",
        "max": max_results,
        "token": NEWS_API_KEY
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        data = response.json()

        if "articles" not in data:
            return {"error": "Invalid response", "raw": data}

        return {"articles": data["articles"]}

    except Exception as error:
        return {"error": str(error)}