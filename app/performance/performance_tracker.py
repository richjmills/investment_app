from datetime import datetime, timezone

from app.portfolio.fx import get_usd_eur_rate
from app.portfolio.valuation import calculate_holding_value


def _utc_today() -> str:
    return datetime.now(timezone.utc).date().isoformat()


def calculate_portfolio_value(portfolio: dict) -> float:
    cash = float(portfolio.get("cash", 0))
    holdings = portfolio.get("holdings", [])

    usd_eur_rate = get_usd_eur_rate()

    holdings_value = 0.0
    for holding in holdings:
        holdings_value += calculate_holding_value(holding, usd_eur_rate)

    return round(cash + holdings_value, 2)


def evaluate_performance(current_value: float, baseline_value: float) -> dict:
    if baseline_value <= 0:
        return {
            "status": "No baseline",
            "absolute_return_pct": None,
            "cagr_target": 5.5,
            "performance_band": "Unknown"
        }

    absolute_return_pct = round(((current_value - baseline_value) / baseline_value) * 100, 2)

    if absolute_return_pct > 6.5:
        performance_band = "Above Target"
    elif absolute_return_pct >= 4.5:
        performance_band = "On Track"
    elif absolute_return_pct >= 2.0:
        performance_band = "Below Target"
    else:
        performance_band = "Significantly Below"

    return {
        "status": "OK",
        "as_of": _utc_today(),
        "current_value": current_value,
        "baseline_value": baseline_value,
        "absolute_return_pct": absolute_return_pct,
        "cagr_target": 5.5,
        "performance_band": performance_band
    }