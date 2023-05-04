import unittest
from datetime import datetime
from models import *


class Test_StateModel(unittest.TestCase):
    """
    Test the state model class
    """

    def test_minimal_creation(self):
        """creating an object with no arguments"""
        model = State()
        self.assertTrue(hasattr(model, "name"))
        self.assertTrue(hasattr(model, "id"))
        self.assertTrue(hasattr(model, "created_at"))

    def test_var_initialization(self):
        """Check default type"""
        model = State()
        self.assertIsInstance(model.created_at, datetime)

    def test_save(self):
        """Try to save the object to storage"""
        test_state = {'id': "009",
                      'created_at': datetime(2017, 2, 12, 00, 31, 55, 331997),
                      'name': "TEST STATE FOR STATE"}
        state = State(test_state)
        state.save()
        storage.delete(state)


if __name__ == "__main__":
    unittest.main()
