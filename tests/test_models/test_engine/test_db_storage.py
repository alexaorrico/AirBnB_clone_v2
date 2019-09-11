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
import random
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
    @unittest.skipIf(models.storage_t != 'db',
                     "testing db storage instead of file")
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(models.storage.all()), dict)

    @unittest.skipIf(models.storage_t != 'db',
                     "testing db storage instead of file")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""

    @unittest.skipIf(models.storage_t != 'db',
                     "testing db storage instead of file")
    def test_new(self):
        """test that new adds an object to the database"""

    @unittest.skipIf(models.storage_t != 'db',
                     "testing db storage instead of file")
    def test_save(self):
        """Test that save properly saves objects to file.json"""

    @unittest.skipIf(models.storage_t != 'db',
                     "testing db storage instead of file")
    def test_get_none(self):
        """Test to check if None is returned if bad parameters are passed
        or if object is not found in storage"""
        instance = models.storage
        self.assertIs(instance.get("State", None), None)
        self.assertIs(instance.get(None, "123"), None)
        self.assertIs(instance.get("Bologna", "34hr8943r389r34r"), None)
        self.assertIs(instance.get([1, 2, 3], "24332432424"), None)
        self.assertIs(instance.get("43284923742", [1, 2, 3]), None)

    @unittest.skipIf(models.storage_t != 'db',
                     "testing db storage instead of file")
    def test_get(self):
        """Test to check if obj was correctly grabbed"""
        instance = models.storage
        state_cls = State(name="California")
        instance.new(state_cls)
        self.assertIs(instance.get(state_cls.__class__.__name__,
                                   state_cls.id), state_cls)

    @unittest.skipIf(models.storage_t != 'db',
                     "testing db storage instead of file")
    def test_count(self):
        """Test to check if number of objects returned is correct"""
        instance = models.storage
        dict_of_objs = instance.all()
        num_of_objs = len(dict_of_objs)
        if num_of_objs == 0:
            state_cls = State(name="California")
            instance.new(state_cls)
            self.assertNotEqual(len(instance.all()), 0)
        else:
            state_cls = State(name="California")
            instance.new(state_cls)
            plus_one = len(instance.all())
            self.assertNotEqual(num_of_objs, plus_one)
