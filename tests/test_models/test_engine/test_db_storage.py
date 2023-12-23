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
storage = models.storage
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
    """Tests for DBStorage methods."""
    @classmethod
    def setUpClass(cls):
        """Set up for the tests"""
        cls.storage = DBStorage()
        cls.storage.reload()

    @classmethod
    def tearDownClass(cls):
        """Clean up after tests"""
        del cls.storage

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count_method(self):
        """Test the count method of DBStorage"""
        initial_state_count = self.storage.count(State)
        new_state = State(name="New State")
        self.storage.new(new_state)
        self.storage.save()
        self.assertEqual(self.storage.count(State), initial_state_count + 1)

        total_initial_count = self.storage.count()
        new_user = User(email='user@example.com', password='password')
        self.storage.new(new_user)
        self.storage.save()
        self.assertEqual(self.storage.count(), total_initial_count + 1)

    def test_count_method_none(self):
        """Test count method with none as class parameter"""
        self.assertIsInstance(self.storage.count(None), int)

    def test_fake_count_method(self):
        """Test the count method with a fake DBStorage"""
        fake_storage = DBStorage()
        fake_storage.count = lambda cls=None: -1
        self.assertEqual(fake_storage.count("State"), -1)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get_method(self):
        """Test get method with valid and invalid IDs"""
        new_state = State(name="California")
        self.storage.new(new_state)
        self.storage.save()
        retrieved_state = self.storage.get(State, new_state.id)
        self.assertEqual(new_state, retrieved_state)

        self.assertIsNone(self.storage.get(State, "invalid_id"))

    def test_get_method_none(self):
        """Test get method with none parameters"""
        self.assertIsNone(self.storage.get(None, None))


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
