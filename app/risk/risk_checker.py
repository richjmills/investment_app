from app.portfolio.fx import get_usd_eur_rate
from app.portfolio.valuation import calculate_holding_value


def check_risk(portfolio: dict, strategy_state: dict) -> dict:
    """Basic v1 risk checks."""
    cash = float(portfolio.get("cash", 0))
    holdings = portfolio.get("holdings", [])

    usd_eur_rate = get_usd_eur_rate()

    total_holdings_value = 0.0
    holding_values = []

    for holding in holdings:
        value = calculate_holding_value(holding, usd_eur_rate)
        total_holdings_value += value
        holding_values.append({
            "symbol": holding.get("symbol", "UNKNOWN"),
            "type": holding.get("type", "").lower(),
            "value": value
        })

    total_portfolio_value = total_holdings_value + cash

    if total_portfolio_value == 0:
        return {
            "risk_level": "Unknown",
            "flags": ["No portfolio value available"],
            "cash_weight": 0,
            "max_single_position": 0,
            "crypto_weight": 0
        }

    cash_weight = round((cash / total_portfolio_value) * 100, 2)

    max_single_position = 0.0
    flags = []

    for item in holding_values:
        weight = round((item["value"] / total_portfolio_value) * 100, 2)
        item["weight"] = weight

        if weight > max_single_position:
            max_single_position = weight

        if weight > 10:
            flags.append(f"{item['symbol']} exceeds max single position limit ({weight}%)")

    crypto_weight = 0.0
    for item in holding_values:
        if item["type"] == "crypto":
            crypto_weight += item["weight"]

    if crypto_weight > 30:
        flags.append(f"Crypto exceeds max allocation limit ({round(crypto_weight, 2)}%)")

    if cash_weight < 5:
        flags.append(f"Cash below minimum floor ({cash_weight}%)")

    if max_single_position > 15 or cash_weight < 5:
        risk_level = "Elevated"
    else:
        risk_level = "Normal"

    return {
        "risk_level": risk_level,
        "flags": flags,
        "cash_weight": cash_weight,
        "max_single_position": round(max_single_position, 2),
        "crypto_weight": round(crypto_weight, 2)
    }