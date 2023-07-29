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

    @unittest.skipIf(models.storage_t != 'db', "not testing fs storage")
    @classmethod
    def setUpClass(cls):
        """Set up the test environment"""
        storage._FileStorage__objects = {}
        cls.db_storage = DBStorage()
        cls.db_storage.reload()

    @unittest.skipIf(models.storage_t != 'db', "not testing fs storage")
    @classmethod
    def tearDownClass(cls):
        """Tear down the test environment"""
        cls.db_storage.close()

    @unittest.skipIf(models.storage_t != 'db', "not testing fs storage")
    def setUp(self):
        """Set up before each test"""
        # Start a new database session for each test
        self.db_storage.reload()

    @unittest.skipIf(models.storage_t != 'db', "not testing fs storage")
    def tearDown(self):
        """Tear down after each test"""
        # Remove the database session after each test
        for obj in list(self.db_storage.all().values()):
            self.db_storage.delete(obj)
        self.db_storage.save()
        self.db_storage.close()

    @unittest.skipIf(models.storage_t != 'db', "not testing fs storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionary"""
        self.assertIs(type(self.db_storage.all()), dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing fs storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""
        # Add some objects to the database
        obj1 = State(name="California")
        obj2 = City(name="San Francisco", state_id=obj1.id)
        self.db_storage.new(obj1)
        self.db_storage.new(obj2)
        self.db_storage.save()

        # Fetch all objects from the database
        all_objects = self.db_storage.all()

        # Ensure the objects are retrieved correctly
        self.assertEqual(len(all_objects), 2)

    @unittest.skipIf(models.storage_t != 'db', "not testing fs storage")
    def test_new(self):
        """Test that new adds an object to the database"""
        # Create a new object and save it to the database
        obj = State(name="New York")
        self.db_storage.new(obj)
        self.db_storage.save()

        # Ensure the object is stored in the database
        all_objects = self.db_storage.all(State)
        self.assertEqual(len(all_objects), 1)

    @unittest.skipIf(models.storage_t != 'db', "not testing fs storage")
    def test_save(self):
        """Test that save properly saves objects to the database"""
        # Create a new object and save it to the database
        obj = State(name="Texas")
        self.db_storage.new(obj)
        self.db_storage.save()

        # Ensure the object is stored in the database
        all_objects = self.db_storage.all(State)
        self.assertEqual(len(all_objects), 1)

    @unittest.skipIf(models.storage_t != 'db', "not testing fs storage")
    def test_count_all(self):
        """Test that count properly counts all objects"""
        obj1 = State(name="Florida")
        obj2 = State(name="Georgia")
        self.db_storage.new(obj1)
        self.db_storage.new(obj2)
        self.db_storage.save()

        # Count all objects in the database
        count_all = self.db_storage.count()

        # Ensure the count is correct
        self.assertEqual(count_all, 2)

    @unittest.skipIf(models.storage_t != 'db', "not testing fs storage")
    def test_count_by_class(self):
        """Test that count() works if given a class"""
        obj1 = State(name="Illinois")
        obj2 = City(name="Chicago", state_id=obj1.id)
        obj3 = City(name="Springfield", state_id=obj1.id)
        self.db_storage.new(obj1)
        self.db_storage.new(obj2)
        self.db_storage.new(obj3)
        self.db_storage.save()

        # Count objects of State class in the database
        count_states = self.db_storage.count(State)

        # Ensure the count is correct
        self.assertEqual(count_states, 1)

    @unittest.skipIf(models.storage_t != 'db', "not testing fs storage")
    def test_get_existing_object(self):
        """Test that get returns the object with the given id"""
        # Create a new State object and add it to the database
        state = State(name="texas")
        self.db_storage.new(state)
        self.db_storage.save()

        # Get the State object using the get method and its id
        result_state = self.db_storage.get(State, state.id)

        # Assert that the returned object is the same as the original
        self.assertEqual(result_state, state)

    @unittest.skipIf(models.storage_t != 'db', "not testing fs storage")
    def test_get_non_existing_object(self):
        """Test that get returns None for a non-existing object"""
        # Get a non-existing object using a random id
        state = State(name="texas")
        self.db_storage.new(state)
        self.db_storage.save()

        result_state = self.db_storage.get(State, "1234566732")

        # Assert that the result is None since the object does not exist
        self.assertIsNone(result_state)


if __name__ == '__main__':
    unittest.main()
