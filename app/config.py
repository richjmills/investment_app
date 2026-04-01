from pathlib import Path
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Data paths
DATA_DIR = BASE_DIR / "data"
LOG_DIR = BASE_DIR / "logs"

STRATEGY_STATE_PATH = DATA_DIR / "strategy_state.json"
PORTFOLIO_PATH = DATA_DIR / "portfolio.json"

# Log file
LOG_FILE = LOG_DIR / "app.log"

# API keys (empty for now)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MARKET_API_KEY = os.getenv("MARKET_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")