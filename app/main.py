from app.config import PORTFOLIO_PATH, STRATEGY_STATE_PATH
from app.logger import setup_logger
from app.scheduler import run_scheduler
from app.state_manager import load_portfolio, load_strategy_state


def main():
    logger = setup_logger()

    logger.info("Starting Investment App")

    strategy_state = load_strategy_state()
    portfolio = load_portfolio()

    logger.info("Strategy state loaded from: %s", STRATEGY_STATE_PATH)
    logger.info("Portfolio loaded from: %s", PORTFOLIO_PATH)
    logger.info("Current regime: %s", strategy_state["current_regime"]["name"])
    logger.info("Portfolio cash: %s", portfolio["cash"])

    run_scheduler(logger, interval_seconds=3600)


if __name__ == "__main__":
    main()