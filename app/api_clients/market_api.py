import requests
import yfinance as yf

from app.config import ALPHA_VANTAGE_API_KEY

BASE_URL = "https://www.alphavantage.co/query"


def get_stock_price_alpha(symbol: str) -> dict:
    params = {
        "function": "GLOBAL_QUOTE",
        "symbol": symbol,
        "apikey": ALPHA_VANTAGE_API_KEY
    }

    response = requests.get(BASE_URL, params=params, timeout=10)
    data = response.json()

    if "Information" in data or "Note" in data:
        raise ValueError("Alpha Vantage rate limited")

    if "Global Quote" not in data or not data["Global Quote"]:
        raise ValueError("Alpha Vantage invalid response")

    quote = data["Global Quote"]

    return {
        "symbol": symbol,
        "price": float(quote["05. price"]),
        "change": float(quote["09. change"]),
        "change_percent": quote["10. change percent"],
        "source": "alpha_vantage"
    }


def get_stock_price_yahoo(symbol: str) -> dict:
    ticker = yf.Ticker(symbol)
    history = ticker.history(period="2d")

    if history.empty:
        raise ValueError(f"Yahoo Finance returned no data for {symbol}")

    latest_close = float(history["Close"].iloc[-1])

    if len(history) > 1:
        previous_close = float(history["Close"].iloc[-2])
        change = latest_close - previous_close
        change_percent = f"{(change / previous_close) * 100:.2f}%"
    else:
        change = 0.0
        change_percent = "0.00%"

    return {
        "symbol": symbol,
        "price": latest_close,
        "change": round(change, 2),
        "change_percent": change_percent,
        "source": "yahoo_finance"
    }


def get_stock_price(symbol: str) -> dict:
    try:
        return get_stock_price_alpha(symbol)
    except Exception:
        try:
            return get_stock_price_yahoo(symbol)
        except Exception as error:
            return {
                "error": f"Both Alpha Vantage and Yahoo Finance failed for {symbol}: {error}"
            }