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

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(models.storage.all()), dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""
        new_obj = State(name='California')
        models.storage.new(new_obj)
        self.assertIn('State.{}'.format(
            new_obj.id), models.storage.all())

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_with_class(self):
        """Test that all returns all rows when a class is passed"""
        new_obj = State(name='California')
        models.storage.new(new_obj)
        self.assertIn('State.{}'.format(
            new_obj.id), models.storage.all(State))

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """test that new adds an object to the database"""
        init_len = len(models.storage.all())
        new_obj = State(name='California')
        new_obj2 = City(name='California', state_id=new_obj.id)
        models.storage.new(new_obj)
        models.storage.new(new_obj2)

        self.assertEqual(init_len + 2, len(models.storage.all()))

        self.assertIn(f'{new_obj.__class__.__name__}.{new_obj.id}',
                      models.storage.all().keys())

        self.assertIn(new_obj, models.storage.all().values())

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get(self):
        """tests that get method retrieves an object from the database"""
        self.assertIsNone(models.storage.get(None, None))
        new_obj = State(name='California')
        models.storage.new(new_obj)

        self.assertIsNone(models.storage.get(None, new_obj.id))
        self.assertIsNone(models.storage.get(State, None))
        self.assertIsNotNone(models.storage.get(State, new_obj.id))
