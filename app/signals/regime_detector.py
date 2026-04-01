from app.signals.theme_detector import detect_themes


def detect_regime() -> str:
    themes = detect_themes()

    inflation = themes.get("inflation", 0)
    rates = themes.get("interest_rates", 0)
    geopolitics = themes.get("geopolitics", 0)
    growth = themes.get("growth", 0)
    risk_on = themes.get("risk_on", 0)
    risk_off = themes.get("risk_off", 0)

    # Risk-off conditions
    if geopolitics >= 5 or (inflation + rates) >= 8:
        return "risk_off"

    # Risk-on conditions
    if growth >= 3 or risk_on > risk_off:
        return "risk_on"

    return "neutral"