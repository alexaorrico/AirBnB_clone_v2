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
    def test_get_method(self):
        """Test the get method for DBStorage"""
        # Create and commit a new object for retrieval
        obj_to_retrieve = BaseModel()
        obj_to_retrieve.save()

        # Retrieve the object using the get method
        retrieved_obj = db_storage.get(BaseModel, obj_to_retrieve.id)

        # Assertions
        self.assertIsNotNone(retrieved_obj, "Object retrieval failed.")
        self.assertEqual(obj_to_retrieve.id, retrieved_obj.id,
                         "Retrieved object ID does not match.")

        # Cleanup
        db_storage.delete(retrieved_obj)
        db_storage.save()

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count_method(self):
        """Test the count method for DBStorage"""
        # Initial count
        initial_count = db_storage.save().count(BaseModel)

        # Create a new object to affect the count
        new_obj = BaseModel()
        new_obj.save()
        initial_count = db_storage.count(BaseModel)


        # New count should be greater by 1
        new_count = db_storage.count(BaseModel)
        self.assertEqual(new_count, initial_count + 1,
                         "Count did not increase after adding an object.")
