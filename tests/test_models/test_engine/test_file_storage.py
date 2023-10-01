#!/usr/bin/python3
"""
Contains the TestFileStorageDocs classes
"""

import unittest
from models import storage
from models.state import State

class TestFileStorageMethods(unittest.TestCase):
"""Tests to check the documentation and style of FileStorage class"""

    def test_get_existing_object(self):
        # Test retrieving an existing object
        new_state = State(name="Test State")
        storage.new(new_state)
        storage.save()
        retrieved_state = storage.get(State, new_state.id)
        self.assertEqual(retrieved_state, new_state)

    def test_get_non_existing_object(self):
        # Test retrieving a non-existing object
        non_existent_id = "non_existent_id"
        retrieved_state = storage.get(State, non_existent_id)
        self.assertIsNone(retrieved_state)

    def test_count_all_objects(self):
        # Test counting all objects in storage
        initial_count = storage.count()
        new_state = State(name="Test State")
        storage.new(new_state)
        storage.save()
        updated_count = storage.count()
        self.assertEqual(updated_count, initial_count + 1)

    def test_count_specific_objects(self):
        # Test counting specific objects in storage
        initial_count = storage.count(State)
        new_state = State(name="Test State")
        storage.new(new_state)
        storage.save()
        updated_count = storage.count(State)
        self.assertEqual(updated_count, initial_count + 1)

if __name__ == '__main__':
    unittest.main()
