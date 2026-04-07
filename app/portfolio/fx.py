from app.ingestion.market_ingestor import load_market_data


def get_usd_eur_rate() -> float:
    market_data = load_market_data()

    entry = market_data.get("USDEUR=X", {})
    data = entry.get("data", {})
    price = data.get("price")

    if price is not None:
        return float(price)

    return 0.92