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


class TestDBStorageMethods(unittest.TestCase):

    def setUp(self):
        """Set up a DBStorage instance for testing."""
        self.storage = DBStorage()

    def tearDown(self):
        """Clean up after each test."""
        self.storage.close()

    def test_get_existing_object(self):
        """Test getting an existing object."""
        # Create a new State object
        state = State(name="Test State")
        state.save()



class TestDBStorageCount(unittest.TestCase):
    """Test the count method in the DBStorage class"""

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                     "not testing db storage")
        # Get the object by its ID
        retrieved_state = self.storage.get(State, state.id)

        # Check that the retrieved object matches the original
        self.assertEqual(retrieved_state.id, state.id)
        self.assertEqual(retrieved_state.name, state.name)

    def test_get_nonexistent_object(self):
        """Test getting a nonexistent object."""
        # Get an object with an ID that doesn't exist
        nonexistent_state = self.storage.get(State, "nonexistent_id")

        # Check that None is returned
        self.assertIsNone(nonexistent_state)

    def test_count_all_objects(self):
        """Test counting all objects in storage."""
        # Create some objects for testing
        State(name="State 1").save()
        State(name="State 2").save()
        State(name="State 3").save()

        # Count all objects
        count = self.storage.count()

        # Check that the count matches the number of created objects
        self.assertEqual(count, 3)


    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                     "not testing db storage")
    def test_count_objects_of_specific_class(self):
        """Test counting objects of a specific class"""
        storage = DBStorage()
        count = storage.count("Amenity")
        self.assertIsInstance(count, int)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                     "not testing db storage")
    def test_count_objects_of_non_existing_class(self):
        """Test counting objects of a non-existing class"""
        storage = DBStorage()
        count = storage.count("NonExistingClass")
        self.assertEqual(count, 0)

    def test_count_objects_of_specific_class(self):
        """Test counting objects of a specific class."""
        # Create some objects for testing
        State(name="State 1").save()
        State(name="State 2").save()
        BaseModel().save()  # Create an object of a different class

        # Count objects of the State class
        count = self.storage.count(State)

        # Check that the count matches the number of created State objects
        self.assertEqual(count, 2)



if __name__ == '__main__':
    unittest.main()
