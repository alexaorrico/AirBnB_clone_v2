#!/usr/bin/python3
"""
Unittest for FileStorage Class
"""
import unittest
from datetime import datetime
import models
from models import engine
from models.engine.file_storage import FileStorage
import json
import os

User = models.user.User
State = models.state.State
City = models.city.City
BaseModel = models.base_model.BaseModel
FileStorage = engine.file_storage.FileStorage
storage = models.storage

@unittest.SkipIf(storage_type == db, 'skip if environ is not db')
class TestGetCountFS(unittest.TestCase):
    """test get and count methods"""
    def setUpClass(cls):
        print('\n\n.................................')
        print('...... Testing Get and Count ......')
        print('.......... FS Methods ..........')
        print('.................................\n\n')

    def setUp(self):
        """initializes new state and cities for testing"""
        if os.path.isfile(F):
            os.remove(F)
        storage.reload()
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

        self.assertEqual(real_state), self.state)
        self.assertNotEqual(fake_state, self.state)

    def test_count(self):
        """Test if count method returns correct numbers"""
        state_count = storage.count("State")
        city_count = storage.count("City")
        place_count = storage.count("Place")

        self.assertEqual(state_count, 1)
        self.assertEqual(city_count, 2)
        self.assertEqual(place_count, 0)


if __name__ == "__main__":
    unittest
