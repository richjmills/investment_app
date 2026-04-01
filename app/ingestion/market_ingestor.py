import json
import time
from datetime import datetime, timezone

from app.api_clients.market_api import get_stock_price
from app.config import DATA_DIR

MARKET_CACHE = DATA_DIR / "market_cache.json"


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_market_data() -> dict:
    """Load cached market data."""
    if not MARKET_CACHE.exists():
        return {}

    with open(MARKET_CACHE, "r", encoding="utf-8") as file:
        return json.load(file)


def update_market_data(symbols: list) -> dict:
    """Fetch market data and keep old cache if a fetch fails."""
    existing_cache = load_market_data()
    results = existing_cache.copy()

    for i, symbol in enumerate(symbols):
        if i > 0:
            time.sleep(12)

        data = get_stock_price(symbol)

        if "error" in data:
            old_entry = existing_cache.get(symbol)
            if old_entry:
                results[symbol] = old_entry
            else:
                results[symbol] = {
                    "data": data,
                    "timestamp": _utc_now_iso()
                }
        else:
            results[symbol] = {
                "data": data,
                "timestamp": _utc_now_iso()
            }

    with open(MARKET_CACHE, "w", encoding="utf-8") as file:
        json.dump(results, file, indent=2)

    return results