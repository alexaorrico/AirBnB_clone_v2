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
from os import getenv
from models.base_model import Base
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

    @unittest.skipIf(models.storage_t != 'db', "not testing file storage")
    def setUp(self):
        """Set up test fixtures for each test"""
        # create a DBStorage object
        # create some entries and save them
        pass

    @unittest.skipIf(models.storage_t != 'db', "not testing file storage")
    def tearDown(self):
        """Clean up after each test"""
        pass

    @unittest.skipIf(models.storage_t != 'db', "not testing file storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(models.storage.all()), dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing file storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""

    @unittest.skipIf(models.storage_t != 'db', "not testing file storage")
    def test_new(self):
        """test that new adds an object to the database"""

    @unittest.skipIf(models.storage_t != 'db', "not testing file storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""
        pass

    @unittest.skipIf(models.storage_t != 'db', "not testing file storage")
    def test_get(self):
        """Test that get returns correct object based on class and id"""
        storage = DBStorage()
        storage.reload()
        new_dict = {}
        for key, value in classes.items():
            instance = value()
            instance_key = instance.__class__.__name__ + "." + instance.id
            new_dict[instance_key] = instance
            storage.new(instance)
        storage.save()
        for key, instance in new_dict.items():
            cls = instance.__class__
            id = instance.id
            with self.subTest(cls=cls, id=id):
                obj = storage.get(cls, id)
                self.assertIsInstance(obj, cls)
                self.assertIs(obj, instance)

    @unittest.skipIf(models.storage_t != 'db', "not testing file storage")
    def test_count_with_class(self):
        """Test that count returns correct number of objects of a particular
        class"""
        storage = DBStorage()
        storage.reload()
        for key, value in classes.items():
            instance = value()
            storage.new(instance)
        storage.save()
        for cls in classes.values():
            with self.subTest(cls=cls):
                total = storage.get(cls=cls)
                self.assertIsInstance(total, int)
                self.assertEqual(total, 1)

    @unittest.skipIf(models.storage_t != 'db', "not testing file storage")
    def test_count_without_class(self):
        """Testing that count returns correct number of total objects in
        storage"""
        storage = DBStorage()
        storage.reload()
        for value in classes.values():
            instance = value()
            storage.new(instance)
        storage.save()
        total = storage.count()
        self.assertIsInstance(total, int)
        self.assertEqual(total, len(classes))
