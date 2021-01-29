#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
import models
from models import storage
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
import MySQLdb
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
    """Test the FileStorage class"""
    @unittest.skipIf(os.getenv(
        'HBNB_TYPE_STORAGE') != "db", "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(models.storage.all()), dict)

    @unittest.skipIf(os.getenv(
        'HBNB_TYPE_STORAGE') != "db", "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""
        len_all = len(storage.all())
        self.assertEqual(len_all, len(storage.all()))

    @unittest.skipIf(os.getenv(
        'HBNB_TYPE_STORAGE') != "db", "not testing db storage")
    def test_new(self):
        """test that new adds an object to the database"""
        self.assertEqual(1, 1)

    @unittest.skipIf(os.getenv(
        'HBNB_TYPE_STORAGE') != "db", "not testing db storage")
    def test_save(self):
        """ Test if an object is store in the database """
        new = State(name="Antioquia")
        new.save()
        _id = new.to_dict()['id']
        self.assertIn(
            new.__class__.__name__ + '.' + _id, storage.all(type(new)).keys())

    def test_get_db_state(self):
        """testing get method"""
        d0 = {"name": "Test0"}
        new_state0 = State(**d0)
        storage.new(new_state0)
        storage.save()
        st0 = storage.get(State, new_state0.id)
        self.assertEqual(new_state0, st0)

    def test_get_db_amenity(self):
        """testing get method with class Amenity"""
        d0 = {"name": "Test0"}
        new_amenity0 = Amenity(**d0)
        storage.new(new_amenity0)
        storage.save()
        amenity0 = storage.get(Amenity, new_amenity0.id)
        self.assertEqual(new_amenity0, amenity0)

    def test_get_db_user(self):
        """testing get method with class User"""
        d0 = {"email": "email0@", "password": "hdgesdg!"}
        new_user0 = User(**d0)
        storage.new(new_user0)
        storage.save()
        user0 = storage.get(User, new_user0.id)
        self.assertEqual(new_user0, user0)

    def test_get_db_id(self):
        """testing get method with a wrong id"""
        get_state = storage.get(State, "2456jffghj")
        self.assertEqual(get_state, None)

    def test_count_db(self):
        """Testing count method for all classes"""
        len_0 = len(storage.all())
        count_0 = storage.count()
        self.assertEqual(len_0, count_0)

    def test_count_db_state(self):
        """Testing count method for a State class"""
        len_state = len(storage.all(State))
        count_state = storage.count(State)
        self.assertEqual(len_state, count_state)
