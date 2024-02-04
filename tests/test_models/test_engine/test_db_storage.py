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

        @classmethod
    def setUpClass(cls):
        """Prepares the test environment before the tests start."""
        storage.reload()

    @classmethod
    def tearDownClass(cls):
        """Cleans up the test environment after the tests have completed."""
        pass

    def setUp(self):
        """Prepares an isolated test environment; called before every test function."""
        self.session = storage._DBStorage__session
        self.session.rollback()  # Ensure each test starts with a clean database state

    def tearDown(self):
        """Cleans up resources after each test."""
        self.session.rollback()

    def test_initialization(self):
        """Test initialization of the DBStorage object."""
        self.assertIsInstance(storage, DBStorage)

    def test_session_creation(self):
        """Test session creation in DBStorage."""
        self.assertIsNotNone(storage._DBStorage__session)

    def test_add_query_object(self):
        """Test adding and querying an object."""
        initial_count = storage.count(State)
        new_state = State(name="TestState")
        storage.new(new_state)
        storage.save()
        self.assertEqual(storage.count(State), initial_count + 1)
        queried_state = storage.get(State, new_state.id)
        self.assertEqual(queried_state.name, "TestState")
        storage.delete(new_state)
        storage.save()
        self.assertEqual(storage.count(State), initial_count)

    def test_update_object(self):
        """Test updating an object."""
        new_state = State(name="UpdateTest")
        storage.new(new_state)
        storage.save()
        new_state.name = "UpdatedName"
        storage.save()
        updated_state = storage.get(State, new_state.id)
        self.assertEqual(updated_state.name, "UpdatedName")
        storage.delete(new_state)
        storage.save()

    def test_add_incomplete_object(self):
        """Test adding an object with missing required fields; should raise an error."""
        incomplete_state = State()
        with self.assertRaises(IntegrityError):
            storage.new(incomplete_state)
            storage.save()

    def test_query_nonexistent_object(self):
        """Test querying a nonexistent object."""
        self.assertIsNone(storage.get(State, "nonexistent_id"))

    def test_state_city_relationship(self):
        """Test the relationship between State and City."""
        new_state = State(name="TestStateForCity")
        new_city = City(name="TestCity", state=new_state)
        storage.new(new_state)
        storage.new(new_city)
        storage.save()
        self.assertIn(new_city, new_state.cities)
        storage.delete(new_city)
        storage.delete(new_state)
        storage.save()

    def test_complex_query_with_filters(self):
        """Test complex queries with filters."""
        state1 = State(name="QueryState1")
        state2 = State(name="QueryState2")
        city1 = City(name="QueryCity1", state=state1)
        city2 = City(name="QueryCity2", state=state2)
        storage.new(state1)
        storage.new(state2)
        storage.new(city1)
        storage.new(city2)
        storage.save()
        filtered_cities = storage._DBStorage__session.query(City).join(State).filter(State.name == "QueryState1").all()
        self.assertIn(city1, filtered_cities)
        self.assertNotIn(city2, filtered_cities)
        storage.delete(city1)
        storage.delete(city2)
        storage.delete(state1)
        storage.delete(state2)
        storage.save()

    def test_deletion_with_foreign_key(self):
        """Test that deleting a State also deletes its cities."""
        state = State(name="DeleteState")
        city = City(name="DeleteCity", state=state)
        storage.new(state)
        storage.new(city)
        storage.save()
        storage.delete(state)
        storage.save()
        self.assertIsNone(storage.get(City, city.id))

    def test_new_feature_method(self):
        """Test the new feature method."""
        state = State(name="PopularState")
        storage.new(state)
        storage.save()
        result = storage.find_most_popular(State)
        self.assertEqual(state, result)
        storage.delete(state)
        storage.save()


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


class TestDBStorageGetCount(unittest.TestCase):
    """Test the get and count methods of the DBStorage class."""

    @classmethod
    def setUpClass(cls):
        """Set up for the tests."""
        models.storage.reload()
        cls.state = State(name="TestState")
        models.storage.new(cls.state)
        models.storage.save()

    @classmethod
    def tearDownClass(cls):
        """Clean up actions after tests."""
        models.storage.delete(cls.state)
        models.storage.save()

    def test_get_method_valid_id(self):
        """Test retrieval of object by valid ID."""
        obj = models.storage.get("State", self.state.id)
        self.assertEqual(obj, self.state)

    def test_get_method_invalid_id(self):
        """Test retrieval with an invalid ID returns None."""
        obj = models.storage.get("State", "invalid_id")
        self.assertIsNone(obj)

    def test_get_method_invalid_class(self):
        """Test retrieval with an invalid class returns None."""
        obj = models.storage.get("InvalidClass", self.state.id)
        self.assertIsNone(obj)

    def test_count_method_with_class(self):
        """Test counting objects of a specific class."""
        initial_count = models.storage.count("State")
        new_state = State(name="AnotherTestState")
        models.storage.new(new_state)
        models.storage.save()
        self.assertEqual(models.storage.count("State"), initial_count + 1)
        models.storage.delete(new_state)
        models.storage.save()

    def test_count_method_no_class(self):
        """Test counting all objects in storage."""
        initial_count = models.storage.count()
        new_state = State(name="YetAnotherTestState")
        models.storage.new(new_state)
        models.storage.save()
        self.assertTrue(models.storage.count() > initial_count)
        models.storage.delete(new_state)
        models.storage.save()
