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
import pycodestyle
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
        style = pycodestyle.StyleGuide(quiet=True)
        result = style.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        style = pycodestyle.StyleGuide(quiet=True)
        result = style.check_files(['tests/test_models/test_engine/\
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
    """Test the FileStorage class"""
    @unittest.skipIf(models.storage_t != 'db', "not testing fs storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(models.storage.all()), dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing fs storage")
    def test_all_no_class(self):
        """Test method all when class is not given"""
        self.assertIs(type(models.storage.all()), dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing fs storage")
    def test_all_class(self):
        """Test method all when class is given"""
        self.assertIs(type(models.storage.all(State)), dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing fs storage")
    def test_new(self):
        """test that new adds an object to the current db session"""
        new_obj = {}
        new_obj["name"] = "Test State"
        new_state = State(**new_obj)
        self.assertIsNone(models.storage.new(new_state))

    @unittest.skipIf(models.storage_t != 'db', "not testing fs storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""
        old_len = len(models.storage.all(State))
        new = {}
        new['name'] = 'Test State'
        test_state = State(**new)
        test_state.save()
        new_len = len(models.storage.all(State))
        self.assertGreater(new_len, old_len)

    @unittest.skipIf(models.storage_t != 'db', "skip test on fs storage")
    def test_delete(self):
        """Test delete object if not None"""
        new = {"name": "Test delete"}
        new = State(**new)
        new.save()
        old_len = len(models.storage.all(State))
        models.storage.delete(new)
        new_len = len(models.storage.all(State))
        self.assertLess(new_len, old_len)

    @unittest.skipIf(models.storage_t != 'db', "skip test on fs storage")
    def test_reload(self):
        """Test that a db session is created and ready for use"""
        self.assertIsNone(models.storage.reload())

    @unittest.skipIf(models.storage_t != 'db', "skip test on fs storage")
    def test_close(self):
        """Test closing db session"""
        self.assertIsNone(models.storage.close())

    @unittest.skipIf(models.storage_t != 'db', "skip test on fs storage")
    def test_get(self):
        """Test get that retrieve one object that belong to a class"""
        new = {"name": "Test get"}
        new = State(**new)
        new.save()
        first_state_id = list(models.storage.all(State).values())[0].id
        state = models.storage.get(State, first_state_id)
        self.assertTrue(state)

    @unittest.skipIf(models.storage_t != 'db', "skip test on fs storage")
    def test_count(self):
        """Test Count object by class or all object in db if class None"""
        total_states_obj = models.storage.count(State)
        total_obj = models.storage.count()
        self.assertGreaterEqual(total_states_obj, 0)
        self.assertGreaterEqual(total_obj, 0)
