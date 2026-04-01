def generate_signals(regime: str, themes: dict) -> dict:
    signals = {
        "action": "hold",
        "confidence": 0,
        "notes": []
    }

    geopolitics = themes.get("geopolitics", 0)
    inflation = themes.get("inflation", 0)
    rates = themes.get("interest_rates", 0)
    growth = themes.get("growth", 0)

    if regime == "risk_off":
        signals["action"] = "de-risk"
        signals["confidence"] = 0.7

        if geopolitics > 7:
            signals["notes"].append("High geopolitical risk")
            signals["confidence"] += 0.1

        if inflation > 3 or rates > 3:
            signals["notes"].append("Inflation / rates pressure")
            signals["confidence"] += 0.1

    elif regime == "risk_on":
        signals["action"] = "increase_risk"
        signals["confidence"] = 0.6

        if growth > 3:
            signals["notes"].append("Growth improving")
            signals["confidence"] += 0.2

    else:
        signals["action"] = "hold"
        signals["confidence"] = 0.5

    return signals