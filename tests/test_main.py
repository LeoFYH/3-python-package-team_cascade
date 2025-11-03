import sys, os, pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from study_pet.__main__ import main


def test_main_start(monkeypatch):
    calls = {"started": False}
    monkeypatch.setattr(
        "study_pet.__main__.start_session", lambda: calls.update(started=True)
    )
    monkeypatch.setattr("sys.argv", ["prog", "start"])
    main()
    assert calls["started"]


def test_main_status(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["prog", "status"])
    monkeypatch.setattr("study_pet.__main__.get_status", lambda: "Pet OK")
    main()
    captured = capsys.readouterr().out
    assert "Pet OK" in captured


def test_main_invalid_command(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["prog", "unknown"])
    main()
    captured = capsys.readouterr().out
    assert "Unknown command" in captured
