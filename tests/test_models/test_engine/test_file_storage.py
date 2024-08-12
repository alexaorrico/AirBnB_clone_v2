#!/usr/bin/python3
"""
Unit tests for FileStorage class
"""
import unittest
from models.engine.file_storage import FileStorage
from models.state import State
from models import storage
import os


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'file', "FileStorage tests")
class TestFileStorage(unittest.TestCase):
    """Tests for FileStorage"""

    def setUp(self):
        """Set up for tests"""
        self.storage = FileStorage()
        self.new_state = State(name="TestState")
        self.storage.new(self.new_state)
        self.storage.save()

    def tearDown(self):
        """Tear down test"""
        self.storage.delete(self.new_state)
        self.storage.save()

    def test_get(self):
        """Test get method"""
        obj = self.storage.get(State, self.new_state.id)
        self.assertEqual(obj, self.new_state)

    def test_count(self):
        """Test count method"""
        state_count = self.storage.count(State)
        self.assertEqual(state_count, 1)
        total_count = self.storage.count()
        self.assertGreaterEqual(total_count, state_count)


if __name__ == '__main__':
    unittest.main()
