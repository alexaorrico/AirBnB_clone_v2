from models import storage
from models.state import State

def test_get_count():
    # Test get() method
    first_state_id = list(storage.all(State).values())[0].id
    first_state = storage.get(State, first_state_id)
    assert isinstance(first_state, State)

    # Test count() method
    all_count = storage.count()
    state_count = storage.count(State)
    assert all_count > 0
    assert state_count > 0

