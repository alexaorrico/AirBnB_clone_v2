#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
from models import storage
import models
from models.engine import db_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
from os import environ, stat
import os
import pep8
import unittest
DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{} method needs a docstring".format(func[0]))


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""
    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(models.storage.all()), dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """test that new adds an object to the database"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""


@unittest.skipIf(models.storage_t != 'db', "not testing db storage")
class TestCountGet(unittest.TestCase):
    """testing Count and Get methods"""

    @classmethod
    def setUpClass(cls):
        """sets up the class for this round of tests"""
        storage.delete_all()
        cls.state = State(name="Centre")
        cls.city = City(state_id=cls.state.id,
                        name="Yaounde")
        cls.user = User(email="oumate.alhadji61@gmail.com",
                        password="pwd")
        cls.place1 = Place(user_id=cls.user.id, city_id=cls.city.id,
                           name="a house")
        cls.place2 = Place(user_id=cls.user.id, city_id=cls.city.id,
                           name="another house")
        cls.amenity1 = Amenity(name="Wifi")
        cls.amenity2 = Amenity(name="fridge")
        cls.amenity3 = Amenity(name="Table")
        objs = [cls.state, cls.city, cls.user, cls.place1, cls.place2,
                cls.amenity1, cls.amenity2, cls.amenity3]
        for obj in objs:
            obj.save()

    def setUp(self):
        """initializes new user for testing"""
        self.city = TestCountGet.city
        self.state = TestCountGet.state
        self.user = TestCountGet.user
        self.place1 = TestCountGet.place1
        self.place2 = TestCountGet.place2
        self.amenity1 = TestCountGet.amenity1
        self.amenity2 = TestCountGet.amenity2
        self.amenity3 = TestCountGet.amenity3

    def test_all_reload_save(self):
        """... checks if all(), save(), and reload function
        in new instance.  This also tests for reload"""
        actual = 0
        db_objs = storage.all()
        for obj in db_objs.values():
            for x in [self.state.id, self.city.id,
                      self.user.id, self.place1.id]:
                if x == obj.id:
                    actual += 1
        self.assertTrue(actual == 4)

    def test_get_pace(self):
        """... checks if get() function returns properly"""
        duplicate = storage.get('Place', self.place1.id)
        expected = self.place1.id
        self.assertEqual(expected, duplicate.id)

    def test_count_amenity(self):
        """... checks if count() returns proper count with Class input"""
        count_amenity = storage.count('Amenity')
        expected = 3
        self.assertEqual(expected, count_amenity)

    def test_count_all(self):
        """... checks if count() functions with no class"""
        count_all = storage.count()
        expected = 8
        self.assertEqual(expected, count_all)


if __name__ == "__main__":
    unittest.main
