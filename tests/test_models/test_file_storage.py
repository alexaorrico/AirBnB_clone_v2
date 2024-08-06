#!/usr/bin/python3
"""
Contains the tests for FileStorage methods get and count
"""

import unittest
from models.engine.file_storage import FileStorage
from models.state import State


class TestFileStorage(unittest.TestCase):
    """
    Tests for the FileStorage class focusing on new get/count functionalities
    """

    @classmethod
    def setUpClass(cls):
        """Set up for the tests"""
        cls.storage = FileStorage()
        cls.state = State(name="California")
        cls.storage.new(cls.state)
        cls.storage.save()

    def test_get(self):
        """Test the get method for FileStorage."""
        self.assertEqual(self.state, self.storage.get(State, self.state.id))

    def test_count(self):
        """Test the count method for FileStorage."""
        initial_count = self.storage.count(State)
        new_state = State(name="Nevada")
        self.storage.new(new_state)
        self.storage.save()
        self.assertEqual(self.storage.count(State), initial_count + 1)
        self.assertEqual(self.storage.count(), None)

    @classmethod
    def tearDownClass(cls):
        """Clean up resources after tests"""
        cls.storage.delete(cls.state)


if __name__ == '__main__':
    unittest.main()
