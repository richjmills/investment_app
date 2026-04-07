from app.ingestion.market_ingestor import load_market_data


def get_live_price(symbol: str) -> float:
    market_data = load_market_data()
    entry = market_data.get(symbol, {})
    data = entry.get("data", {})

    price = data.get("price")
    if price is None:
        return 0.0

    return float(price)


def calculate_holding_value(holding: dict, usd_eur_rate: float = 1.0) -> float:
    quantity = float(holding.get("quantity", 0))
    symbol = holding.get("symbol", "")
    currency = holding.get("currency", "EUR").upper()

    price = get_live_price(symbol)

    if currency == "USD":
        price = price * usd_eur_rate

    return round(quantity * price, 2)