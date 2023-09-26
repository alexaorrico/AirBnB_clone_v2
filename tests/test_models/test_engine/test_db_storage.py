#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
import models
from models.engine import db_storage
from models.engine.db_storage import DBStorage
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

class TestDBStorageGet(unittest.TestCase):
    """Test the get method in DBStorage"""
    def test_get(self):
        """Test the get method"""
        # Create an instance of DBStorage
        storage = DBStorage()

        # Create a test object (e.g., an Amenity instance)
        test_obj = Amenity(name="Test Amenity")
        test_obj.save()

        # Use the get method to retrieve the test object
        retrieved_obj = storage.get(Amenity, test_obj.id)

        # Assert that the retrieved object is not None
        self.assertIsNotNone(retrieved_obj)

        # Assert that the retrieved object has the correct class and ID
        self.assertIsInstance(retrieved_obj, Amenity)
        self.assertEqual(retrieved_obj.id, test_obj.id)

class TestDBStorageCount(unittest.TestCase):
    """Test the count method in DBStorage"""
    def test_count(self):
        """Test the count method"""
        # Create an instance of DBStorage
        storage = DBStorage()

        # Create some test objects (e.g., Amenity instances)
        amenity1 = Amenity(name="Amenity 1")
        amenity2 = Amenity(name="Amenity 2")
        amenity3 = Amenity(name="Amenity 3")

        # Save the test objects
        amenity1.save()
        amenity2.save()
        amenity3.save()

        # Use the count method to count all Amenity objects
        count_all = storage.count(Amenity)

        # Assert that the count is correct
        self.assertEqual(count_all, 3)

        # Use the count method to count all objects (no class specified)
        count_all_objects = storage.count()

        # Assert that the count of all objects is correct
        self.assertEqual(count_all_objects, 3)

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


if __name__ == "__main__":
    storage = DBStorage()
    storage.reload()