from app.strategy.signal_engine import generate_signals

themes = {
    "inflation": 4,
    "interest_rates": 5,
    "geopolitics": 9,
    "growth": 0
}

regime = "risk_off"

print(generate_signals(regime, themes))
