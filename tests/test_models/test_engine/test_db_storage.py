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


@unittest.skipIf(models.storage_t != 'db', "not testing db storage")
class TestDBStorage(unittest.TestCase):
    """Test the FileStorage class"""
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(models.storage.all()), dict)

    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""

    def test_new(self):
        """test that new adds an object to the database"""

    def test_save(self):
        """Test that save properly saves objects to file.json"""

    def test_get(self):
        """test that get returns an object of a specified class by id."""
        storage = models.storage
        obj = User(name='Francis')
        obj.save()
        self.assertEqual(obj.id, storage.get(User, obj.id).id)
        self.assertEqual(obj.name, storage.get(User, obj.id).name)
        self.assertIsNot(obj, storage.get(User, obj.id + 'us'))
        self.assertIsNone(storage.get(User, obj.id + 'us'))
        self.assertIsNone(storage.get(User, 123))
        self.assertIsNone(storage.get(None, obj.id))
        self.assertIsNone(storage.get(int, obj.id))
        with self.assertRaises(TypeError):
            storage.get(User, obj.id, 'op')
        with self.assertRaises(TypeError):
            storage.get(User)
        with self.assertRaises(TypeError):
            storage.get()

    def test_count(self):
        """test that count returns the number of objects of a pecified class."""
        
        storage = models.storage
        
        self.assertIs(type(storage.count(int)), int)
        self.assertIs(type(storage.count()), int)
        self.assertIs(type(storage.count(None)), int)
        self.assertIs(type(storage.count(User)), int)
        self.assertEqual(storage.count(), storage.count(None))
        User(name='Francis').save()
        self.assertGreater(storage.count(User), 0)
        User(name='Anane').save()
        self.assertGreater(storage.count(User), 1)
        self.assertEqual(storage.count(), storage.count(None))
        User(name='Ofori').save()
        count = storage.count(User)
        User(name='Kwame').save()
        self.assertGreater(storage.count(User), count)
        State(name='Ashanti').save()
        self.assertGreater(storage.count(), storage.count(User))
        with self.assertRaises(TypeError):
            storage.count(User, 'id')