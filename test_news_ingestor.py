from app.ingestion.news_ingestor import update_news, load_news

update_result = update_news()
print("UPDATE:", update_result)

cached = load_news()
print("CACHED:", cached)
