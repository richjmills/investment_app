from app.portfolio.fx import get_usd_eur_rate
from app.portfolio.valuation import calculate_holding_value


def evaluate_holdings(portfolio: dict, strategy_state: dict, regime: str) -> dict:
    """Evaluate each holding and generate simple v1 recommendations."""
    cash = float(portfolio.get("cash", 0))
    holdings = portfolio.get("holdings", [])

    usd_eur_rate = get_usd_eur_rate()

    total_holdings_value = 0.0
    parsed_holdings = []

    for holding in holdings:
        symbol = holding.get("symbol", "UNKNOWN")
        asset_type = holding.get("type", "").lower()
        quantity = float(holding.get("quantity", 0))
        value = calculate_holding_value(holding, usd_eur_rate)
        price = value / quantity if quantity > 0 else 0

        total_holdings_value += value
        parsed_holdings.append({
            "symbol": symbol,
            "type": asset_type,
            "quantity": quantity,
            "price": price,
            "value": value
        })

    total_portfolio_value = total_holdings_value + cash

    if total_portfolio_value == 0:
        return {
            "status": "No portfolio value available",
            "evaluations": []
        }

    evaluations = []

    for holding in parsed_holdings:
        weight = round((holding["value"] / total_portfolio_value) * 100, 2)

        recommendation = "hold"
        priority = "Low"
        notes = []

        asset_type = holding["type"]
        symbol = holding["symbol"]

        if weight > 10:
            recommendation = "trim"
            priority = "High"
            notes.append(f"Position exceeds max single-position guideline ({weight}%)")

        if regime == "risk_off":
            if asset_type in ["stock", "etf", "equity", "equities"]:
                notes.append("Equity exposure less attractive in risk_off regime")
                if recommendation == "hold":
                    recommendation = "review"
                    priority = "Medium"

            if asset_type == "crypto":
                recommendation = "reduce"
                priority = "High"
                notes.append("Crypto exposure less attractive in risk_off regime")

            if asset_type in ["gold", "silver", "commodity", "commodities"]:
                notes.append("Commodity / defensive exposure may fit regime better")

        elif regime == "risk_on":
            if asset_type in ["stock", "etf", "equity", "equities"]:
                notes.append("Equity exposure broadly aligned with risk_on regime")

            if asset_type == "crypto":
                notes.append("Crypto can be considered in risk_on regime if sizing is controlled")

        if not notes:
            notes.append("No major issue detected under current simple rules")

        evaluations.append({
            "symbol": symbol,
            "type": asset_type,
            "weight_pct": weight,
            "recommendation": recommendation,
            "priority": priority,
            "notes": notes
        })

    return {
        "status": "OK",
        "evaluations": evaluations
    }