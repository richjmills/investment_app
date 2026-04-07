from app.portfolio.holding_evaluator import evaluate_holdings
from app.state_manager import load_portfolio, load_strategy_state

portfolio = load_portfolio()
strategy_state = load_strategy_state()

# Use the machine-detected or recommended regime for testing
regime = "risk_off"

result = evaluate_holdings(portfolio, strategy_state, regime)

for item in result["evaluations"]:
    print(item)
