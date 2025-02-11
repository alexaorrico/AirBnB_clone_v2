import unittest
from models import storage
from models.state import State


class TestDBStorageGet(unittest.TestCase):
    """Test cases for the get method in DBStorage."""

    @unittest.skipIf(storage.__class__.__name__ != "DBStorage",
                     "not testing db storage")
    def test_get_existing_object(self):
        """Test retrieving an existing object."""
        new_state = State(name="California")
        storage.new(new_state)
        storage.save()
        retrieved_state = storage.get(State, new_state.id)
        self.assertIsNotNone(retrieved_state)
        self.assertEqual(retrieved_state.id, new_state.id)

    @unittest.skipIf(storage.__class__.__name__ != "DBStorage",
                     "not testing db storage")
    def test_get_nonexistent_object(self):
        """Test retrieving a non-existent object."""
        retrieved_state = storage.get(State, "nonexistent_id")
        self.assertIsNone(retrieved_state)

    @unittest.skipIf(storage.__class__.__name__ != "DBStorage",
                     "not testing db storage")
    def test_get_invalid_class(self):
        """Test passing an invalid class to get method."""
        retrieved_obj = storage.get("InvalidClass", "some_id")
        self.assertIsNone(retrieved_obj)


if __name__ == "__main__":
    unittest.main()
