from .tracker import start_session, end_session
from .pet.core import get_status
from .data_manager import reset_state as _reset_state

__all__ = ["start_session", "end_session", "get_status", "reset_pet"]


def reset_pet():
    """Resets all pet data and progress."""
    _reset_state()
    print("🐣 Your pet has been reborn! All progress reset.")
