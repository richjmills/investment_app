from app.actions.action_engine import generate_actions
from app.state_manager import load_portfolio

signal = {
    "action": "de-risk",
    "confidence": 0.9,
    "notes": ["High geopolitical risk", "Inflation / rates pressure"]
}

portfolio = load_portfolio()

print(generate_actions(signal, portfolio))
