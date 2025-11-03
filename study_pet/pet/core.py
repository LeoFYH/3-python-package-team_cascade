"""
study_pet/pet/core.py
-------------------------------------------
Core logic for StudyPet:
Handles leveling, experience, and status updates
based on total study time.

Design principles:
- update_pet(): true update (writes to persistent JSON)
- get_status(): live preview (uses current session time if any, no write)
"""

from ..data_manager import load_state, save_state
from datetime import datetime
import time


def _calculate_level_exp(total_hours: float):
    """
    Convert total study hours to (level, exp).

    Level = floor(total_hours / 5) + 1
    EXP   = (total_hours % 5) * 20
    (Every 5 hours = +1 level, 100 EXP = level up)
    """
    level = int(total_hours // 5) + 1
    exp = (total_hours % 5) * 20
    return level, exp


# called when session ends
def update_pet():
    """
    Performs a *true* update of the pet’s level and experience,
    writing the results to persistent storage.
    """
    state = load_state()
    total_time = state.get("total_study_time", 0.0)
    prev_level = state.get("level", 1)

    new_level, new_exp = _calculate_level_exp(total_time)

    if new_level > prev_level:
        print(f" {state['name']} leveled up! {prev_level} → {new_level}")

    # Update state values
    state["level"] = new_level
    state["experience"] = new_exp
    state["last_study_date"] = datetime.now().strftime("%Y-%m-%d")

    save_state(state)
    return state


# shows real time data
def get_status():
    """
    Does NOT modify the JSON file.
    """
    state = load_state()
    total_time = state.get("total_study_time", 0.0)
    last_start = state.get("last_session_start", None)

    # If currently studying, include elapsed time
    if last_start is not None:
        elapsed = (time.time() - last_start) / 3600
        total_time += elapsed
    else:
        elapsed = 0.0

    # compute simulate  level/exp
    level, exp = _calculate_level_exp(total_time)

    name = state.get("name", "Unnamed")
    mood = state.get("mood", 100)
    streak = state.get("streak_days", 0)
    last_study = state.get("last_study_date", "N/A")

    studying = "Studying now" if last_start else " Idle"

    status = (
        f"\n Pet Status (Live Preview)\n"
        f"Name: {name}\n"
        f"Level: {level} ({exp:.0f} EXP)\n"
        f"Total Study Time: {total_time:.2f} hrs (+{elapsed:.2f}h current)\n"
        f"Last Study: {last_study}\n"
        f"Mood: {mood}/100    Streak: {streak} days\n"
        f"Session: {studying}"
    )

    return status


#  Manual test
if __name__ == "__main__":
    print("🔁 Checking pet status preview...")
    print(get_status())
