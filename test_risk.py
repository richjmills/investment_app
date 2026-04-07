from app.risk.risk_checker import check_risk
from app.state_manager import load_portfolio, load_strategy_state

portfolio = load_portfolio()
strategy_state = load_strategy_state()

result = check_risk(portfolio, strategy_state)
print(result)
