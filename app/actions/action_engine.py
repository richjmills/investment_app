def generate_actions(signal: dict, portfolio: dict) -> dict:
    action_type = signal.get("action", "hold")
    confidence = signal.get("confidence", 0)
    notes = signal.get("notes", [])

    recommendations = []

    holdings = portfolio.get("holdings", [])
    cash = portfolio.get("cash", 0)

    if action_type == "de-risk":
        recommendations.append("Do not add new risk")
        recommendations.append("Review high-beta or cyclical holdings")
        recommendations.append("Consider raising cash gradually")
        recommendations.append("Prefer defensive positioning")

    elif action_type == "increase_risk":
        recommendations.append("Look for opportunities to add risk gradually")
        recommendations.append("Prioritise strongest themes and leaders")
        recommendations.append("Use staged entries rather than all at once")

    else:
        recommendations.append("Hold current positioning")
        recommendations.append("Wait for clearer regime confirmation")

    return {
        "signal": action_type,
        "confidence": confidence,
        "portfolio_cash": cash,
        "holding_count": len(holdings),
        "notes": notes,
        "recommendations": recommendations
    }