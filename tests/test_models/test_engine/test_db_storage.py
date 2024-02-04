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
    def test_get_method(self):
        """Tests the get method"""
        # Create some test objects
        city_obj = City()
        state_obj = State()

        # Add objects to FileStorage
        self.file_storage.new(city_obj)
        self.file_storage.new(state_obj)

        # Test getting objects by id and class
        retrieved_city = self.file_storage.get(City, city_obj.id)
        retrieved_state = self.file_storage.get(State, state_obj.id)

        self.assertEqual(retrieved_city, city_obj)
        self.assertEqual(retrieved_state, state_obj)

        # Test getting non-existent object
        non_existent_obj = self.file_storage.get(City, "nonexistent_id")
        self.assertIsNone(non_existent_obj)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count_method(self):
        """Tests the count method"""
        # Create some test objects
        city_obj1 = City()
        city_obj2 = City()
        state_obj = State()

        # Add objects to FileStorage
        self.file_storage.new(city_obj1)
        self.file_storage.new(city_obj2)
        self.file_storage.new(state_obj)

        # Test counting all objects
        total_objects = self.file_storage.count()
        self.assertEqual(total_objects, 3)

        # Test counting objects of a specific class
        city_objects_count = self.file_storage.count(City)
        self.assertEqual(city_objects_count, 2)

        state_objects_count = self.file_storage.count(State)
        self.assertEqual(state_objects_count, 1)

        # Test counting non-existent class
        non_existent_class_count = self.file_storage.count(int)
        self.assertEqual(non_existent_class_count, 0)
