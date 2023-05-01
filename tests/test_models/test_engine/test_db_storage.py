#!/usr/bin/python3
"""Test for DBStorage"""
import unittest
import os
from models import *
from models.base_model import Base
from models.engine.db_storage import DBStorage


class TestGetCountDB(unittes.TestCase):
    """test get and count methods"""

    @classmethod
    def setUpClass(cls):
        print('\n\n.................................')
        print('...... Testing Get and Count ......')
        print('.......... DB Methods ..........')
        print('.................................\n\n')

    def setUp(self):
        """initializes new state and cities for testing"""
        
        self.state = State()
        self.state.name = 'California'
        self.state.save()
        self.city1 = City()
        self.city1.name = 'Fremont'
        self.city1.state_id = self.state.id
        self.city1.save()
        self.city2 = City()
        self.city2.name = 'San_Francisco'
        self.city2.state_id = self.state.id
        self.city2.save()

    def test_get(self):
        """Test if get method returns state"""
        real_state = storage.get("State", self.state.id)
        fake_state = storage.get("State", "12345")
        no_state = storage.get("", "")

        self.assertEqual(real_state, self.state)
        self.assertNotEqual(fake_state, self.state)
        self.assertIsNone(no_state)

    def test_count(self):
        """Tests if count method returns correct numbers"""
        state_count = storage.count("State")
        city_count = storage.count("City")
        place_count = storage.count("Place")
        all_count = storage.count(None)

        self.assertEqual(state_count, 1)
        self.assertEqual(city_count, 2)
        self.assertEqual(place_count, 0)
        self.assertEqual(all_count, 18)


if __name__ == "__main__":
    unittest
