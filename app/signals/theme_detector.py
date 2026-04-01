from app.ingestion.news_ingestor import load_news


THEMES = {
    "inflation": ["inflation", "prices rising", "cost pressures"],
    "interest_rates": ["interest rate", "rate hike", "rate cut", "fed"],
    "geopolitics": ["war", "conflict", "tariffs", "china", "iran"],
    "growth": ["growth", "expansion", "strong economy"],
    "risk_off": ["selloff", "risk aversion", "market fall"],
    "risk_on": ["rally", "stocks rise", "bullish"]
}


def detect_themes() -> dict:
    news = load_news()
    articles = news.get("articles", [])

    theme_scores = {theme: 0 for theme in THEMES}

    for article in articles:
        text = f"{article.get('title', '')} {article.get('description', '')}".lower()

        for theme, keywords in THEMES.items():
            for keyword in keywords:
                if keyword in text:
                    theme_scores[theme] += 1

    return theme_scores