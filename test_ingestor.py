from app.ingestion.market_ingestor import update_market_data, load_market_data

symbols = ["AAPL"]

result = update_market_data(symbols)
print("UPDATE RESULT:", result)

cached = load_market_data()
print("CACHED RESULT:", cached)