import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from study_pet import hello
from study_pet.tracker import track


def test_hello():
    assert "Hello" in hello()


def test_track():
    assert "Tracking" in track()
