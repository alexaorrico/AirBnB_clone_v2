#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
import models
from models.engine import file_storage
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
FileStorage = file_storage.FileStorage
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


# tests for v3
class TestDBStorage(unittest.TestCase):
    """Test DBstorage"""
    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db')
    def test_get(self):
        """Test if get returns an object or not"""
        new_state = State(name="mystate")
        new_state.save()
        new_user = User(email="userbla@gmail.com", password="password")
        new_user.save()
        self.assertIs(new_state, models.storage.get("State", new_state.id))
        self.assertIs(None, models.storage.get("State", "dfituosdh"))
        self.assertIs(None, models.storage.get("qkgkq", "qdsjfghjks"))
        self.assertIs(new_user, models.storage.get("User", new_user.id))
        self.assertIs(None, models.storage.get("User", "sdogiuzo"))

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db')
    def test_count(self):
        """Test if count returns the number of objects"""
        first = models.storage.count()
        self.assertEqual(models.storage.count("shdgkshj", 0))
        new_state = State(name="mystate")
        new_state.save()
        new_user = User(email="userbla@gmail.com", password="password")
        new_user.save()
        new_user2 = User(email="userbla2@gmail.com", password="password")
        new_user2.save()
        self.assertEqual(models.storage.count("State"), first + 1)
        self.assertEqual(models.storage.count("User"), first + 2)
        self.assertEqual(models.storage.count(), first + 3)
