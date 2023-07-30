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
classes = [State, City, Place, Amenity, Review, User]


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to pep8."""
        pep = pep8.StyleGuide(quiet=True)
        result = pep.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to pep8."""
        pep = pep8.StyleGuide(quiet=True)
        result = pep.check_files(['tests/test_models/test_engine/\
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
    @unittest.skipIf(models.storage_t != 'db', "not testing FILE storage")
    def setUp(self):
        """Setup for test"""
        self.storage = DBStorage()
        self.storage.reload()
        self.test_args = {'name': 'Test'}
        self.obj = State(**self.test_args)
        self.obj_key = "{}.{}".format(self.obj.__class__.__name__, self.obj.id)
        self.storage.new(self.obj)
        self.new_obj = {}
        self.new_obj[self.obj_key] = self.obj

    @unittest.skipIf(models.storage_t != 'db', "not testing FILE storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        new_dict = self.storage.all()
        self.assertEqual(type(new_dict), dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing FILE storage")
    def test_all_class(self):
        """Test that all returns all rows when no class is passed"""
        all_dict = self.storage.all()
        session = self.storage._DBStorage__session
        test_all_dict = {}
        for row in classes:
            for obj in session.query(row).all():
                key = "{}.{}".format(obj.__class__.__name__, obj.id)
                test_all_dict[key] = obj
        self.assertTrue(all_dict == test_all_dict, "not equal")

    @unittest.skipIf(models.storage_t != 'db', "not testing FILE storage")
    def test_new(self):
        """test that new adds an object to the database"""
        all_objs = self.storage.all()
        self.assertLessEqual(self.new_obj.items(), all_objs.items())

    @unittest.skipIf(models.storage_t != 'db', "not testing FILE storage")
    def test_save(self):
        """Test that save properly saves objects to database"""
        self.storage.save()
        self.storage.close()
        new_session = DBStorage()
        new_session.reload()
        new_session_all_objs = new_session.all()
        self.assertLessEqual(self.new_obj.keys(), new_session_all_objs.keys())

    @unittest.skipIf(models.storage_t != 'db', "not testing FILE storage")
    def test_get(self):
        """ Test that get works properly and get right obj"""
        id = self.obj.id
        get_obj = self.storage.get(State, id)
        self.assertEqual(get_obj, self.obj)

    @unittest.skipIf(models.storage_t != 'db', "not testing FILE storage")
    def test_count(self):
        """ Check if count method counts objects right"""
        all_objs = self.storage.all(State)
        count = self.storage.count(State)
        test_count = 0
        for objs in all_objs:
            test_count = test_count + 1
        self.assertEqual(count, test_count)
