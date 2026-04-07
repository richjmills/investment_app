import time

from app.actions.action_engine import generate_actions
from app.ingestion.market_ingestor import update_market_data
from app.ingestion.news_ingestor import update_news
from app.signals.regime_detector import detect_regime
from app.signals.theme_detector import detect_themes
from app.state_manager import load_portfolio, load_strategy_state, save_strategy_state
from app.strategy.signal_engine import generate_signals
from app.portfolio.allocation_checker import check_allocation
from app.risk.risk_checker import check_risk
from app.portfolio.holding_evaluator import evaluate_holdings
from datetime import datetime
from app.performance.performance_tracker import calculate_portfolio_value, evaluate_performance
from app.portfolio.holding_evaluator import evaluate_holdings
from app.reporting.daily_report import build_daily_report
from pathlib import Path
from app.notifications.email_sender import send_daily_report
import json

def should_generate_daily_report(last_report_date: str | None, report_hour: int = 19) -> bool:
    now = datetime.now()
    today_str = now.date().isoformat()

    if last_report_date == today_str:
        return False

    return now.hour >= report_hour


def save_daily_report(report_text: str) -> str:
    reports_dir = Path("data/reports")
    reports_dir.mkdir(parents=True, exist_ok=True)

    filename = f"daily_report_{datetime.now().strftime('%Y-%m-%d')}.txt"
    report_path = reports_dir / filename

    report_path.write_text(report_text, encoding="utf-8")
    return str(report_path)

def run_scheduler(logger, interval_seconds: int = 3600) -> None:
    """Run the main update loop."""
    logger.info("Scheduler started. Update interval: %s seconds", interval_seconds)
    last_report_date = None

    try:
        while True:
            # --- LOAD STATE ---
            portfolio = load_portfolio()
            strategy_state = load_strategy_state()

            symbols = [h["symbol"] for h in portfolio.get("holdings", [])]

            if "USDEUR=X" not in symbols:
                symbols.append("USDEUR=X")

            # --- MARKET DATA ---
            logger.info("Starting scheduled market update")
            market_result = update_market_data(symbols)

            priced_count = 0
            failed_symbols = []

            for symbol, payload in market_result.items():
                data = payload.get("data", {})
                if "error" in data:
                    failed_symbols.append(symbol)
                else:
                    priced_count += 1

            logger.info(
                "Market update complete: %s priced, %s failed",
                priced_count,
                len(failed_symbols)
            )

            if failed_symbols:
                logger.info("Failed symbols: %s", ", ".join(failed_symbols))

            # --- NEWS ---
            news_result = update_news()
            logger.info(
                "News update complete: %s articles",
                len(news_result.get("articles", []))
            )

            # --- THEMES ---
            themes = detect_themes()
            logger.info("Theme summary: %s", themes)

            # --- REGIME + SIGNAL ---
            regime = detect_regime()
            signals = generate_signals(regime, themes)

            current_regime = strategy_state.get("current_regime", {}).get("name")

            if regime != current_regime:
                logger.info(
                    "Regime recommendation detected: %s -> %s",
                    current_regime,
                    regime
                )

                strategy_state["pending_regime_review"] = {
                    "active": True,
                    "candidate_regime": regime,
                    "confidence": "Medium",
                    "flagged_on": "today",
                    "reason": signals["notes"],
                    "status": "Awaiting user review"
                }
                save_strategy_state(strategy_state)

            # --- SIGNAL OUTPUT ---
            logger.info(
                "SIGNAL: %s (confidence: %.2f)",
                signals["action"],
                signals["confidence"]
            )
            logger.info("Signal notes: %s", signals["notes"])

            # --- ALLOCATION CHECK ---
            allocation = check_allocation(portfolio, strategy_state)

            logger.info("ALLOCATION SUMMARY:")
            logger.info("Current: %s", allocation["current_weights"])
            logger.info("Target: %s", allocation["target_weights"])
            logger.info("Deviation: %s", allocation["deviations"])

            if allocation.get("flags"):
                logger.info("ALLOCATION FLAGS:")
                for flag in allocation["flags"]:
                    logger.info("- %s", flag)

                logger.info(
                    "Allocation misalignment detected — review alongside signal"
                )
            risk = check_risk(portfolio, strategy_state)

            logger.info("RISK SUMMARY: %s", risk["risk_level"])
            logger.info(
                "Risk metrics: cash=%s%%, max_single_position=%s%%, crypto=%s%%",
                risk["cash_weight"],
                risk["max_single_position"],
                risk["crypto_weight"]
            )

            if risk.get("flags"):
                logger.info("RISK FLAGS:")
                for flag in risk["flags"]:
                    logger.info("- %s", flag)

            holding_review = evaluate_holdings(portfolio, strategy_state, regime)

            logger.info("HOLDING REVIEW:")
            for item in holding_review.get("evaluations", []):
                logger.info(
                    "%s | %s | %s | %s%%",
                    item["symbol"],
                    item["recommendation"],
                    item["priority"],
                    item["weight_pct"]
                )
                for note in item["notes"]:
                    logger.info("- %s", note)
                    
            # --- ACTIONS ---
            actions = generate_actions(signals, portfolio)

            logger.info("ACTIONS:")
            for recommendation in actions.get("recommendations", []):
                logger.info("- %s", recommendation)


                        # --- DAILY REPORT (end-of-day only) ---
            now = datetime.now()
            today_str = now.date().isoformat()

            if should_generate_daily_report(last_report_date, report_hour=19):    
                with open("data/performance_baseline.json", "r", encoding="utf-8") as file:
                    baseline = json.load(file)

                current_value = calculate_portfolio_value(portfolio)
                performance = evaluate_performance(current_value, baseline["baseline_value"])

                holding_review = evaluate_holdings(portfolio, strategy_state, regime)

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

                report_path = save_daily_report(report)

                email_result = send_daily_report(report_path)
                logger.info("Email status: %s", email_result)

                logger.info("END OF DAY REPORT GENERATED")
                logger.info("Report saved to: %s", report_path)
                print(report)

                last_report_date = today_str

            # --- LOOP ---
            logger.info("Sleeping for %s seconds", interval_seconds)
            time.sleep(interval_seconds)

    except KeyboardInterrupt:
        logger.info("Scheduler stopped by user")