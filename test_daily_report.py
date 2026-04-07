import json

from app.actions.action_engine import generate_actions
from app.performance.performance_tracker import calculate_portfolio_value, evaluate_performance
from app.portfolio.allocation_checker import check_allocation
from app.portfolio.holding_evaluator import evaluate_holdings
from app.risk.risk_checker import check_risk
from app.reporting.daily_report import build_daily_report
from app.signals.regime_detector import detect_regime
from app.signals.theme_detector import detect_themes
from app.state_manager import load_portfolio, load_strategy_state
from app.strategy.signal_engine import generate_signals

portfolio = load_portfolio()
strategy_state = load_strategy_state()

themes = detect_themes()
regime = detect_regime()
signals = generate_signals(regime, themes)

allocation = check_allocation(portfolio, strategy_state)
risk = check_risk(portfolio, strategy_state)
holding_review = evaluate_holdings(portfolio, strategy_state, regime)
actions = generate_actions(signals, portfolio)

current_value = calculate_portfolio_value(portfolio)
with open("data/performance_baseline.json", "r", encoding="utf-8") as file:
    baseline = json.load(file)
performance = evaluate_performance(current_value, baseline["baseline_value"])

report = build_daily_report(
    strategy_state=strategy_state,
    themes=themes,
    regime=regime,
    signals=signals,
    allocation=allocation,
    risk=risk,
    holding_review=holding_review,
    performance=performance,
    actions=actions
)

print(report)
