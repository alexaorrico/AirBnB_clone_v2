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


class TestDBStorage(unittest.TestCase):
    """Test the DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up the class with necessary configurations."""
        # Configure DBStorage for testing
        models.storage.reload()

    def test_get_method(self):
        """Test the get method in DBStorage"""
        # Create an example object to store in the database
        example_obj = State(name="ExampleState")
        example_obj.save()

        # Use get method to retrieve the object by class and ID
        retrieved_obj = models.storage.get(State, example_obj.id)

        # Check if the retrieved object matches the original object
        self.assertEqual(retrieved_obj, example_obj)

    def test_get_method_nonexistent_object(self):
        """Test the get method with a nonexistent object"""
        # Use get method with a class and ID that do not exist
        retrieved_obj = models.storage.get(State, "nonexistent_id")

        # Check if the method returns None for nonexistent objects
        self.assertIsNone(retrieved_obj)

    def test_count_method(self):
        """Test the count method in DBStorage"""
        # Create several example objects to store in the database
        State(name="State1").save()
        State(name="State2").save()
        State(name="State3").save()

        # Use count method to get the number of State objects
        count_states = models.storage.count(State)

        # Check if the count matches the number of created State objects
        self.assertEqual(count_states, 3)

    def test_count_method_all_objects(self):
        """Test the count method without specifying a class"""
        # Create objects of different classes to store in the database
        State(name="State").save()
        City(name="City").save()
        User(username="User").save()

        # Use count method to get the total number of objects
        count_all_objects = models.storage.count()

        # Check if the count matches the total number of created objects
        self.assertEqual(count_all_objects, 3)


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
