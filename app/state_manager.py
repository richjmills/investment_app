import json
from datetime import datetime, timezone
from pathlib import Path

from app.config import PORTFOLIO_PATH, STRATEGY_STATE_PATH


def _utc_now_iso() -> str:
    """Return current UTC time in ISO format."""
    return datetime.now(timezone.utc).isoformat()


def _write_json(path: Path, data: dict) -> None:
    """Write JSON safely with pretty formatting."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)


def _read_json(path: Path, default_data: dict) -> dict:
    """
    Read JSON safely.
    If file is missing, empty, or invalid, recreate it with defaults.
    """
    if not path.exists():
        _write_json(path, default_data)
        return default_data.copy()

    try:
        content = path.read_text(encoding="utf-8").strip()
        if not content:
            _write_json(path, default_data)
            return default_data.copy()

        data = json.loads(content)
        if not isinstance(data, dict):
            _write_json(path, default_data)
            return default_data.copy()

        return data

    except (json.JSONDecodeError, OSError):
        _write_json(path, default_data)
        return default_data.copy()


def default_strategy_state() -> dict:
    """Default v1 strategy state."""
    return {
        "regime": {
            "current": "unconfirmed",
            "last_manual_update": None,
            "notes": ""
        },
        "approved_themes": [],
        "watch_items": [],
        "risk_flags": [],
        "targets": {
            "annual_return_goal": 0.055
        },
        "last_updated": _utc_now_iso()
    }


def default_portfolio() -> dict:
    """Default v1 portfolio structure."""
    return {
        "base_currency": "EUR",
        "cash": 0.0,
        "holdings": []
    }


def load_strategy_state() -> dict:
    """Load strategy state from file."""
    return _read_json(STRATEGY_STATE_PATH, default_strategy_state())


def save_strategy_state(state: dict) -> None:
    """Save strategy state to file."""
    state["last_updated"] = _utc_now_iso()
    _write_json(STRATEGY_STATE_PATH, state)


def load_portfolio() -> dict:
    """Load portfolio from file."""
    return _read_json(PORTFOLIO_PATH, default_portfolio())


def save_portfolio(portfolio: dict) -> None:
    """Save portfolio to file."""
    _write_json(PORTFOLIO_PATH, portfolio)

def save_strategy_state(state: dict) -> None:
    """Save strategy state to file."""
    import json

    with open(STRATEGY_STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)    