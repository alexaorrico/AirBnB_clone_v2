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
    """Test the FileStorage class"""
    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def setUp(self):
        """ Prepare database for testing"""
        self.storage = DBStorage()
        self.test_dict = {}
        self.instance_key = []
        for key, value in classes.items():  # Populate storage with class objs
            with self.subTest(key=key, value=value):
                instance = value()
                self.instance_key.append(instance.__class__.__name__
                                         + "."
                                         + instance.id)
                self.storage.new(instance)
                self.test_dict[instance_key] = instance

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def tearDown(self):
        """Close database after testing"""
        self.storage.close()

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(models.storage.all()), dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all() returns all objects when no class is passed"""
        all_dict = self.storage.all()
        self.assertEqual(test_dict, all_dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """test that new adds an object to the database"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get(self):
        self.assertEqual(self.test_dict, self.storage.all())
        i = o
        for clss in classes:  # test all objs saved in self.storage
            get_obj = list(self.storage.get(cls, self.instance_key[i]))
            cls_obj = self.storage._DBStorage__session.query(classes
                                                             [clss]).all()
            self.assertEqual(get_obj, cls_obj)
            i += 1

        # if no class is passed to get()
        get_obj = self.storage.get(self.instance_key[0])
        self.assertIsNone(get_obj)
        # if a valid class is passed to get() as a string
        get_obj = self.storage.get('Amenity', self.instance_key[0])
        cls_obj = self.storage._DBStorage__session.query(classes
                                                         ['Amenity']).all()
        self.assertIsNotNone(get_obj)
        self.assertEqual(get_obj, cls_obj)  # will likely fail
        # if an invalid/unknown class is passed to get()
        get_obj = self.storage.get('Unknown', self.instance_key[0])
        self.assertIsNone(get_obj)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_count(self):
        """Test the no of objs returned by count()"""
        # there should be only one object per class
        total_objs = len(self.test_dict)
        total_objs = self.storage.count()
        self.assertEqual(total_keys, total_objs)
