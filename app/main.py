from app.config import STRATEGY_STATE_PATH, PORTFOLIO_PATH
from app.logger import setup_logger
from app.state_manager import load_strategy_state, load_portfolio
from app.scheduler import run_scheduler


def main():
    logger = setup_logger()

    logger.info("Starting Investment App")

    # Load core data
    strategy_state = load_strategy_state()
    portfolio = load_portfolio()

    logger.info(f"Strategy state loaded from: {STRATEGY_STATE_PATH}")
    logger.info(f"Portfolio loaded from: {PORTFOLIO_PATH}")

    logger.info(f"Current regime: {strategy_state['regime']['current']}")
    logger.info(f"Portfolio cash: {portfolio['cash']}")

    # Start scheduler loop
    run_scheduler(logger, interval_seconds=300)


if __name__ == "__main__":
    main()