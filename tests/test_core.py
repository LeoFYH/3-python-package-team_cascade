import sys, os, pytest
from datetime import datetime

# 确保导入路径正确
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from study_pet.pet.core import update_pet, get_status
from study_pet.data_manager import load_state, save_state, reset_state


@pytest.fixture(autouse=True)
def clean_state():
    reset_state()
    yield
    reset_state()


def test_update_pet_increases_level():
    state = load_state()
    state["total_study_time"] = 10.0  # 10小时 = 等级3
    save_state(state)

    new_state = update_pet()
    assert new_state["level"] >= 3


def test_update_pet_sets_last_study_date():
    update_pet()
    state = load_state()
    today = datetime.now().strftime("%Y-%m-%d")
    assert state["last_study_date"] == today


def test_get_status_reflects_live_session_time(monkeypatch):
    state = load_state()
    state["total_study_time"] = 2.0
    state["last_session_start"] = 0
    save_state(state)

    monkeypatch.setattr("time.time", lambda: 3600)
    status = get_status()
    assert "3.00" in status or "2.99" in status
