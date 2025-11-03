import json
import os

DATA_DIR = os.path.expanduser("~/.study_pet")
DATA_PATH = os.path.join(DATA_DIR, "data.json")

default_state = {
    "name": "PomPom",
    "level": 1,
    "experience": 0.0,
    "total_study_time": 0.0,
    "last_session_start": None,
    "last_study_date": None,
    "mood": 100,
    "streak_days": 0,
    "money": 0,
    "last_collect_time": None,
    "last_feed_date": None,
    "last_open_date": None,
}


def ensure_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR, exist_ok=True)


def load_state():
    """ """
    ensure_data_dir()
    if not os.path.exists(DATA_PATH):
        save_state(default_state)
    try:
        with open(DATA_PATH, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        save_state(default_state)
        return default_state.copy()


def save_state(state: dict):
    ensure_data_dir()
    with open(DATA_PATH, "w") as f:
        json.dump(state, f, indent=4)


def reset_state():
    save_state(default_state.copy())


if __name__ == "__main__":
    print("📁 Checking data directory:", DATA_DIR)
    reset_state()
    print("✅ Pet data initialized at:", DATA_PATH)
    print("📂 Current state:", load_state())
