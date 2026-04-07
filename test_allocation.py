from app.portfolio.allocation_checker import check_allocation
from app.state_manager import load_portfolio, load_strategy_state

portfolio = load_portfolio()
strategy_state = load_strategy_state()

result = check_allocation(portfolio, strategy_state)
print(result)
