#!/usr/bin/python3
""" test case """
import unittest
from models.city import City
from models.state import State
from models.engine import db_storage
from models.amenity import Amenity
import os


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', "skip if fs")
class TestGet(unittest.TestCase):
    """ test of get method """

    def setUp(self):
        self.storage = db_storage.DBStorage()
        self.storage.reload()
        self.new_state = State(name="California")
        self.new_state.save()
        self.new_city = City(name="San Francisco", state_id=self.new_state.id)
        self.new_city.save()

    def tearDown(self):
        """Tear down after the tests"""
        self.storage.delete(self.new_city)
        self.storage.delete(self.new_state)
        self.storage.save()
        self.storage.close()

    def test_get_existing_object(self):
        """Test get() with an object that exists"""
        obj = self.storage.get(City, self.new_city.id)
        self.assertEqual(obj.id, self.new_city.id)

    def test_get_nonexistent_object(self):
        """Test get() with an object that does not exist"""
        obj = self.storage.get(State, "nonexistent")
        self.assertIsNone(obj)


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', "skip if not db")
class TestDBStorageCount(unittest.TestCase):
    """Tests the count() method of the DBStorage class"""

    def setUp(self):
        """Set up for the tests"""

        self.storage = db_storage.DBStorage()
        self.storage.reload()
        self.new_state1 = State(name="California")
        self.new_state2 = State(name="New York")
        self.new_state3 = State(name="Texas")
        self.new_state1.save()
        self.new_state2.save()
        self.new_state3.save()

    def tearDown(self):
        """Tear down after the tests"""

        self.storage.delete(self.new_state1)
        self.storage.delete(self.new_state2)
        self.storage.delete(self.new_state3)
        self.storage.save()
        self.storage.close()

    def test_count_all_objects(self):
        """Test count() with no arguments"""
        count = self.storage.count()
        self.assertEqual(count, 3)

    def test_count_some_objects(self):
        """Test count() with a class argument"""
        count = self.storage.count(State)
        self.assertEqual(count, 3)

    def test_count_nonexistent_class(self):
        """Test count() with a nonexistent class argument"""
        count = self.storage.count(Amenity)
        self.assertEqual(count, 0)


class TestCaseDb(unittest.TestCase):
    """ just a test for get method """

    def test_format(self):
        # test that work
        pass

