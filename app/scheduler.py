import time
from app.ingestion.market_ingestor import update_market_data
from app.state_manager import load_portfolio
from app.ingestion.news_ingestor import update_news
from app.signals.regime_detector import detect_regime
from app.state_manager import save_strategy_state, load_strategy_state
from app.signals.theme_detector import detect_themes
from app.strategy.signal_engine import generate_signals
from app.actions.action_engine import generate_actions


def run_scheduler(logger, interval_seconds: int = 300) -> None:
    """
    Simple scheduler loop for v1.
    Updates market data, then waits for next cycle.
    Stop with Ctrl+C.
    """
    logger.info("Scheduler started. Update interval: %s seconds", interval_seconds)

    try:
        while True:
            portfolio = load_portfolio()
            symbols = [h["symbol"] for h in portfolio.get("holdings", [])]

            logger.info("Starting scheduled market update")
            market_result = update_market_data(symbols)
            logger.info("Market update complete: %s", market_result)

            news_result = update_news()
            logger.info(
                "News update complete: %s articles",
                len(news_result.get("articles", []))
            )

            themes = detect_themes()
            logger.info("Theme summary: %s", themes)

            regime = detect_regime()
            signals = generate_signals(regime, themes)
            actions = generate_actions(signals, portfolio)

            logger.info("ACTIONS:")
            for rec in actions["recommendations"]:
                logger.info(f"- {rec}")

            logger.info(
                "SIGNAL: %s (confidence: %.2f)",
                signals["action"],
                signals["confidence"]
            )
            logger.info("Signal notes: %s", signals["notes"])

            regime = detect_regime()

            state = load_strategy_state()
            previous_regime = state.get("regime", {}).get("current")

            if regime != previous_regime:
                logger.info("Regime change detected: %s → %s", previous_regime, regime)

            state["regime"]["current"] = regime
            save_strategy_state(state)

            logger.info("Sleeping for %s seconds", interval_seconds)
            time.sleep(interval_seconds)

    except KeyboardInterrupt:
        logger.info("Scheduler stopped by user")