#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
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
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


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
    def test_get(self):
        """Test the get() method"""
        # Create a State object and add it to the database
        state = State(name="California")
        self.storage.new(state)
        self.storage.save()

        # Try to retrieve the State object
        state_id = state.id
        result = self.storage.get(State, state_id)

        # Check that the retrieved object matches the original
        self.assertEqual(state, result)

        # Try to retrieve a non-existent object
        result = self.storage.get(City, "fake_id")
        self.assertIsNone(result)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count(self):
        """Test the count() method"""
        # Create several objects of different classes
        # and add them to the database
        state1 = State(name="California")
        state2 = State(name="Texas")
        city1 = City(name="San Francisco", state_id=state1.id)
        city2 = City(name="Los Angeles", state_id=state1.id)
        city3 = City(name="Houston", state_id=state2.id)
        user1 = User(email="test1@example.com", password="password1")
        user2 = User(email="test2@example.com", password="password2")
        user3 = User(email="test3@example.com", password="password3")
        self.storage.new(state1)
        self.storage.new(state2)
        self.storage.new(city1)
        self.storage.new(city2)
        self.storage.new(city3)
        self.storage.new(user1)
        self.storage.new(user2)
        self.storage.new(user3)
        self.storage.save()

        # Test counting all objects
        result = self.storage.count()
        self.assertEqual(result, 8)

        # Test counting objects of a specific class
        result = self.storage.count(State)
        self.assertEqual(result, 2)
        result = self.storage.count(City)
        self.assertEqual(result, 3)
        result = self.storage.count(User)
        self.assertEqual(result, 3)
        result = self.storage.count(Place)
        self.assertEqual(result, 0)
