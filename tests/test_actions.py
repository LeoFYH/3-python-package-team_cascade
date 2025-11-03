import sys, os, time, pytest, builtins
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from study_pet.pet.actions import rename_pet, collect_money, feed_pet
from study_pet.data_manager import load_state, save_state, reset_state


@pytest.fixture(autouse=True)
def clean_state():
    reset_state()
    yield
    reset_state()


def test_rename_pet_interactive(monkeypatch):
    monkeypatch.setattr(builtins, "input", lambda _: "Fluffy")
    rename_pet()
    state = load_state()
    assert state["name"] == "Fluffy"


def test_collect_money_adds_balance(monkeypatch):
    state = load_state()
    start_money = state["money"]
    collect_money()
    state = load_state()
    assert state["money"] > start_money


def test_collect_money_respects_cooldown(monkeypatch, capsys):
    state = load_state()
    state["last_collect_time"] = time.time()
    save_state(state)
    collect_money()
    captured = capsys.readouterr().out
    assert "You can collect again" in captured


def test_feed_pet_increases_mood(monkeypatch):
    state = load_state()
    state["money"] = 500
    state["mood"] = 60
    save_state(state)

    inputs = iter(["1"])  # Apple
    monkeypatch.setattr(builtins, "input", lambda _: next(inputs))
    feed_pet()
    new_state = load_state()
    assert new_state["mood"] > 60


def test_feed_pet_insufficient_funds(monkeypatch, capsys):
    state = load_state()
    state["money"] = 0
    save_state(state)
    inputs = iter(["1"])
    monkeypatch.setattr(builtins, "input", lambda _: next(inputs))
    feed_pet()
    captured = capsys.readouterr().out
    assert "Not enough coins" in captured
