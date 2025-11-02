"""

Records when the user starts and ends a session,
and updates total study time in the global JSON file.
"""

import time
from .data_manager import load_state, save_state


def start_session():
    """
    Marks the beginning of a study session.
    Stores the current timestamp in the state file.
    """
    state = load_state()
    if state.get("last_session_start") is not None:
        print("Warning: A session is already running!")
        return

    state["last_session_start"] = time.time()
    save_state(state)
    print("Study session started!")


def end_session():
    """
    Ends the study session, calculates duration,
    and updates total study time in hours.
    """
    state = load_state()
    start_time = state.get("last_session_start")

    if start_time is None:
        print("No active study session found.")
        return

    end_time = time.time()
    duration = (end_time - start_time) / 3600  # convert seconds to hours
    state["total_study_time"] += duration
    state["last_session_start"] = None

    save_state(state)
    print(f"Great Job! You studied for {duration:.2f} hours.")
    print(f"Total study time: {state['total_study_time']:.2f} hours.")


def get_total_time():
    """
    Returns the total accumulated study time (in hours).
    """
    state = load_state()
    return state.get("total_study_time", 0.0)


# temp testing code
if __name__ == "__main__":
    print("=== Study Session Tracker Test ===")
    start_session()
    print("Simulating study for 3 seconds...")
    time.sleep(10)  # Simulate a study session of 10 seconds
    end_session()
    print("Total study time:", get_total_time(), "hours")
