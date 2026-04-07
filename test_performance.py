import json

from app.performance.performance_tracker import calculate_portfolio_value, evaluate_performance
from app.state_manager import load_portfolio

portfolio = load_portfolio()
current_value = calculate_portfolio_value(portfolio)

with open("data/performance_baseline.json", "r", encoding="utf-8") as file:
    baseline = json.load(file)

result = evaluate_performance(current_value, baseline["baseline_value"])
print(result)
