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


# rename_pet(): correct 
def test_rename_pet_interactive(monkeypatch):
    monkeypatch.setattr(builtins, "input", lambda _: "Fluffy")
    rename_pet()
    state = load_state()
    assert state["name"] == "Fluffy"

# rename_pet(): invalid input 
def test_rename_pet_empty(monkeypatch, capsys):
    # name should be unchanged if user input is empty
    state = load_state()
    state["name"] = "Fluffy"
    save_state(state)

    monkeypatch.setattr(builtins, "input", lambda _: "")
    rename_pet()

    captured = capsys.readouterr().out
    new_state = load_state()

    
    assert "Name cannot be empty." in captured
    assert new_state["name"] == "Fluffy" 


# collect_money(): correct case
def test_collect_money_adds_balance(monkeypatch):
    state = load_state()
    start_money = state["money"]
    collect_money()
    state = load_state()
    assert state["money"] > start_money

# collect_money(): invalid case
def test_collect_money_respects_cooldown(monkeypatch, capsys):
    state = load_state()
    state["last_collect_time"] = time.time()
    save_state(state)
    collect_money()
    captured = capsys.readouterr().out
    assert "You can collect again" in captured

# feed_pet(): correct case
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

# feed_pet(): invalid case - insufficient funds
def test_feed_pet_insufficient_funds(monkeypatch, capsys):
    state = load_state()
    state["money"] = 0
    save_state(state)
    inputs = iter(["1"])
    monkeypatch.setattr(builtins, "input", lambda _: next(inputs))
    feed_pet()
    captured = capsys.readouterr().out
    assert "Not enough coins" in captured

# feed_pet(): invalid case - invalid menu item 
def test_feed_pet_invalid_choice(monkeypatch, capsys):
    state = load_state()
    state["money"] = 500
    save_state(state)

    monkeypatch.setattr(builtins, "input", lambda _: "9")
    feed_pet()

    captured = capsys.readouterr().out
    assert "Invalid choice" in captured

# feed_pet(): menu item 6 - custom food success 
def test_feed_pet_custom_food(monkeypatch):
    state = load_state()
    state["money"] = 500
    state["mood"] = 80
    save_state(state)

    inputs = iter(["6", "pancakes"])
    monkeypatch.setattr(builtins, "input", lambda _: next(inputs))

    feed_pet()
    new_state = load_state()
    assert new_state["mood"] > 80
    assert new_state["money"] < 500  

# feed_pet(): menu item 6 - custom food empty
def test_feed_pet_custom_food_empty_name(monkeypatch, capsys):
    # if user input is empty, mystery meal
    state = load_state()
    state["money"] = 500
    save_state(state)

    inputs = iter(["6", ""])
    monkeypatch.setattr(builtins, "input", lambda _: next(inputs))

    feed_pet()
    captured = capsys.readouterr().out
    assert "mystery meal" in captured

# feed_pet(): menu item 7 - return 
def test_feed_pet_return(monkeypatch):
    # no state change should happen
    state = load_state()
    state["money"] = 500
    state["mood"] = 50
    save_state(state)

    monkeypatch.setattr(builtins, "input", lambda _: "7")
    feed_pet()
    new_state = load_state()

    assert new_state["money"] == 500
    assert new_state["mood"] == 50