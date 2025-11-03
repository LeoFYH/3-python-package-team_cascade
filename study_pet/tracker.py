"""
Tracks study sessions for StudyPet.

Responsible for:
- Starting and ending sessions
- Updating total study time
- Triggering pet updates (level, exp)
"""

import atexit
import signal
import time
from datetime import datetime
from .data_manager import load_state, save_state
from .pet.core import update_pet


def start_session():
    """
    Begins a study session.
    If a session is already active, it will not start a new one.
    """
    state = load_state()

    if state.get("last_session_start"):
        print("A study session is already active.")
        return

    state["last_session_start"] = time.time()
    save_state(state)
    print(f"📘 Study session started at {datetime.now().strftime('%H:%M:%S')}")


def end_session():
    """
    Ends a study session and updates total study time.
    Also triggers a pet level/exp update.
    """
    state = load_state()
    start_time = state.get("last_session_start", None)

    if not start_time:
        print("⚠️ No active study session found.")
        return

    # Calculate elapsed time in hours
    end_time = time.time()
    elapsed_hours = (end_time - start_time) / 3600

    # Update totals
    state["total_study_time"] += elapsed_hours
    state["last_session_start"] = None
    state["last_study_date"] = datetime.now().strftime("%Y-%m-%d")

    save_state(state)
    print(f"Study session ended. Duration: {elapsed_hours:.2f} hours")

    # Trigger pet update
    update_pet()
    print("Pet data updated!")


def reset_sessions():
    """
    For testing or restarting — clears active session flag.
    """
    state = load_state()
    state["last_session_start"] = None
    save_state(state)
    print("Session reset complete.")


def get_total_time():
    """Returns the total study time stored in JSON (for tests)."""
    state = load_state()
    return state.get("total_study_time", 0.0)


# Manual test
if __name__ == "__main__":
    print("Study Tracker CLI")
    print("1. start_session()")
    print("2. end_session()")
    print("3. reset_sessions()")

manual_close = False


def _auto_end_session(*args):
    state = load_state()
    if state.get("last_session_start") and not manual_close:
        print("\n Auto-saving your progress...")
        end_session()


# autosave on exit or interrupt
atexit.register(_auto_end_session)
signal.signal(signal.SIGINT, _auto_end_session)
signal.signal(signal.SIGTERM, _auto_end_session)
