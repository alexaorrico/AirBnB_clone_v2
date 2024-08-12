#!/usr/bin/python3
"""
Unit tests for DBStorage class
"""
import unittest
from models.engine.db_storage import DBStorage
from models.state import State
from models import storage
import os


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', "DBStorage tests")
class TestDBStorage(unittest.TestCase):
    """Tests for DBStorage"""

    def setUp(self):
        """Set up for tests"""
        self.storage = DBStorage()
        self.storage.reload()
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
