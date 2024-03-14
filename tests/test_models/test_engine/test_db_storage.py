#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
import models
from models.engine.file_storage import FileStorage
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
        result = pep8s.check_files(
            ['tests/test_models/test_engine/test_db_storage.py'])
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
        """Test that all returns all rows when no class is passed """
        db = models.storage
        self.assertNotEqual(db.all(), {})

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_with_class(self):
        """ Tests all() with a class parameter passed """
        db = models.storage
        state_obj = [obj for obj in db.all(State).keys()]
        key = state_obj[0].split('.')[0]
        self.assertEqual(key, "State")

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """test that new adds an object to the database"""
        db = models.storage
        ini = len(db.all(State))
        state = State(name='Abia')
        db.new(state)
        db.save()
        end = len(db.all(State))
        self.assertTrue(end > ini)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """ Test that save properly saves objects to the database """
        db = models.storage
        state = State(name='Lagos')
        db.new(state)
        db.save()
        state_objs = db.all(State)
        key = "{}.{}".format(State.__name__, state.id)
        self.assertIn(key, state_objs.keys())

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_delete(self):
        """ Tests that delete() deletes an obj from the current session """
        db = models.storage
        state = State(name='Anambra')
        db.new(state)
        db.save()
        db.delete(state)
        state_objs = db.all(State)
        key = "{}.{}".format(State.__name__, state.id)
        self.assertNotIn(key, state_objs.keys())

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_reload(self):
        """ tests if reload() recreates objs in the db """
        db = DBStorage()
        db.reload()
        end = len(db.all())
        self.assertFalse(end == 0)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get_with_id_None(self):
        """ Tests if get() retrieves an object when id is None """
        db = models.storage
        state = State(name='Texas')
        ret = db.get(State, None)
        self.assertEqual(ret, None)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get_with_wrongID(self):
        """ Tests get() with a wrong id """
        db = models.storage
        ret = db.get(State, "abc-def")
        self.assertEqual(ret, None)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get_with_ID(self):
        db = models.storage
        state = State(name='London')
        state.save()
        ret = db.get(State, state.id)
        self.assertEqual(ret, state)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count(self):
        """ Tests the count() """
        db = models.storage
        state = State(name='Ontario')
        state2 = State(name='Canada')
        city = City(name='West Ham', state_id=state.id)
        state.save()
        state2.save()
        city.save()
        self.assertFalse(db.count() == db.count(State))
