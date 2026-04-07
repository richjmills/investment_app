from app.portfolio.fx import get_usd_eur_rate
from app.portfolio.valuation import calculate_holding_value


def check_allocation(portfolio: dict, strategy_state: dict) -> dict:
    """Compare current portfolio weights to active targets."""
    cash = float(portfolio.get("cash", 0))
    holdings = portfolio.get("holdings", [])

    usd_eur_rate = get_usd_eur_rate()

    totals = {
        "equities": 0.0,
        "crypto": 0.0,
        "commodities": 0.0,
        "cash": cash
    }

    for holding in holdings:
        asset_type = holding.get("type", "").lower()
        value = calculate_holding_value(holding, usd_eur_rate)

        if asset_type in ["stock", "etf", "equity", "equities"]:
            totals["equities"] += value
        elif asset_type in ["crypto"]:
            totals["crypto"] += value
        elif asset_type in ["commodity", "commodities", "gold", "silver"]:
            totals["commodities"] += value

    total_value = sum(totals.values())

    if total_value == 0:
        return {
            "total_value": 0,
            "current_weights": {},
            "target_weights": strategy_state.get("active_targets", {}),
            "deviations": {},
            "flags": [],
            "status": "No portfolio value to assess"
        }

    current_weights = {
        key: round((value / total_value) * 100, 2)
        for key, value in totals.items()
    }

    target_weights = strategy_state.get("active_targets", {})

    deviations = {}
    for asset_class, target in target_weights.items():
        current = current_weights.get(asset_class, 0)
        deviations[asset_class] = round(current - float(target), 2)

    flags = []
    for asset_class, deviation in deviations.items():
        if deviation > 10:
            flags.append(f"{asset_class} significantly overweight (+{deviation}%)")
        elif deviation < -10:
            flags.append(f"{asset_class} significantly underweight ({deviation}%)")

    return {
        "total_value": round(total_value, 2),
        "current_weights": current_weights,
        "target_weights": target_weights,
        "deviations": deviations,
        "flags": flags,
        "status": "OK"
    }