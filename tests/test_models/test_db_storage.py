#!/usr/bin/python3
"""
Contains the tests for DBStorage methods get and count
"""

import unittest
from models import storage
from models.state import State


class TestDBStorage(unittest.TestCase):
    """
    Tests for the DBStorage class focusing on new get/count functionalities
    """

    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.state = State(name="California")
        storage.new(cls.state)
        storage.save()

    def test_get(self):
        """Test the get method for DBStorage."""
        self.assertEqual(self.state, storage.get(State, self.state.id))

    def test_count(self):
        """Test the count method for DBStorage."""
        initial_count = storage.count(State)
        new_state = State(name="Nevada")
        storage.new(new_state)
        storage.save()
        self.assertEqual(storage.count(State), initial_count + 1)
        self.assertEqual(storage.count(), None)

    @classmethod
    def tearDownClass(cls):
        """Clean up resources after tests"""
        storage.delete(cls.state)


if __name__ == '__main__':
    unittest.main()
