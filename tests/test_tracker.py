import sys, os
import time
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from study_pet.tracker import (
    start_session,
    end_session,
    get_total_time,
    reset_sessions,
    manual_close,
    _auto_end_session,
)
from study_pet.data_manager import load_state, reset_state, save_state


@pytest.fixture(autouse=True)
def clean_data_file():
    reset_state()
    yield
    reset_state()


def test_start_session_creates_timestamp():
    start_session()
    state = load_state()
    assert state["last_session_start"] is not None


def test_end_session_updates_total_time():
    start_session()
    time.sleep(0.5)
    end_session()
    state = load_state()
    assert state["total_study_time"] > 0
    assert state["last_session_start"] is None


def test_get_total_time_matches_state():
    state = load_state()
    state["total_study_time"] = 12.34
    save_state(state)
    total_time = get_total_time()
    assert abs(total_time - 12.34) < 0.001


def test_reset_sessions_clears_active_session():

    start_session()
    reset_sessions()
    state = load_state()
    assert state["last_session_start"] is None


def test_end_session_without_start_does_not_crash():
    try:
        end_session()
        assert True
    except Exception as e:
        pytest.fail(f"end_session() raised an unexpected exception: {e}")


def test_auto_end_session_respects_manual_close(monkeypatch):
    start_session()
    monkeypatch.setattr("study_pet.tracker.manual_close", True)
    _auto_end_session()
    state = load_state()
    # still active because manual close skipped
    assert state["last_session_start"] is not None
