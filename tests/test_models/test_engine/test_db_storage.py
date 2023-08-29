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


class TestDBStorageGet(unittest.TestCase):
    """Test the get method in DBStorage"""

    def test_get_object(self):
        new_state = State(name="California")
        models.storage.new(new_state)
        models.storage.save()

        state_get = models.storage.get(State, new_state.id)
        self.assertEqual(state_get, new_state)

    def test_get_object_inexistente(self):
        state_get = models.storage.get(State, "id_inexistente")
        self.assertIsNone(state_get)


class TestDBStorageCount(unittest.TestCase):
    """Test the count method in DBStorage"""

    def test_count_all(self):
        """Test count method for all objects"""
        initial_count = models.storage.count()
        new_state = State(name="Texas")
        models.storage.new(new_state)
        models.storage.save()
        updated_count = models.storage.count()
        self.assertEqual(updated_count, initial_count + 1)

    def test_count_by_class(self):
        """Test count method for objects by class"""
        new_state = State(name="Florida")
        models.storage.new(new_state)
        models.storage.save()
        updated_count = models.storage.count(State)
        self.assertEqual(updated_count, 1)

    def test_count_nonexistent_class(self):
        """Test count method for nonexistent class"""
        count = models.storage.count()
        self.assertEqual(count, 0)

    def test_count_multiple_objects(self):
        """Test count method for multiple objects"""
        new_state1 = State(name="California")
        new_state2 = State(name="New York")
        models.storage.new(new_state1)
        models.storage.new(new_state2)
        models.storage.save()
        updated_count = models.storage.count(State)
        self.assertEqual(updated_count, 2)
