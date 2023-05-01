#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
import models
from os import getenv
from models import storage
from models.engine import db_storage
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pep8
import unittest
DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}
HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')


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
        """Test tests/test_models/test_engine/test_db_storage.py
        conforms to PEP8."""
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
    """
    Test suite for the DBStorage class.
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up the testing environment.
        """
        storage.reload()

    def tearDown(self):
        """
        Tear down the test case.
        """
        objects = storage.all()
        for obj in objects.values():
            storage.delete(obj)
        storage.save()

    @classmethod
    def tearDownClass(cls):
        """
        Tear down the testing environment.
        """
        storage.close()

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """
        Tests that the all() method returns a dictionary.
        """
        result = storage.all()
        self.assertIsInstance(result, dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_returns_all_objects(self):
        """
        Tests that the all() method returns all objects.
        """
        state = State(name="California")
        storage.new(state)
        storage.save()
        result = storage.all()
        self.assertIn(state, result.values())

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_returns_objects_of_given_class(self):
        """
        Tests that the all() method returns only objects of the given class.
        """
        state = State(name="California")
        user = User(email="test@example.com", password="password")
        storage.new(state)
        storage.new(user)
        storage.save()
        result = storage.all(State)
        self.assertIn(state, result.values())
        self.assertNotIn(user, result.values())

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new_adds_object_to_session(self):
        """
        Tests that the new() method adds an object to the
        current database session.
        """
        state = State(name="California")
        storage.new(state)
        self.assertIn(state, storage._DBStorage__session)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save_commits_changes_to_database(self):
        """
        Tests that the save() method commits changes to the database.
        """
        state = State(name="California")
        storage.new(state)
        storage.save()
        self.assertIn(state, storage.all().values())

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_delete_removes_object_from_database(self):
        """
        Tests that the delete() method removes an object from the database.
        """
        state = State(name="California")
        storage.new(state)
        storage.save()
        storage.delete(state)
        self.assertNotIn(state, storage.all().values())

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_reload_loads_objects_from_database(self):
        """
        Tests that the reload() method loads objects from the database.
        """
        state = State(name="California")
        state.save()
        storage.reload()
        result = storage.get(State, state.id)
        self.assertEqual(len(storage.all()), 1)
        self.assertTrue(result)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get_returns_object_with_given_id(self):
        """
        Tests that the get() method returns an object with the given ID.
        """
        state = State(name="California")
        storage.new(state)
        storage.save()
        result = storage.get(State, state.id)
        self.assertEqual(state, result)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count_returns_number_of_objects(self):
        """
        Tests that the count() method returns the number of
        objects in the database.
        """
        state = State(name="California")
        storage.new(state)
        storage.save()
        result = storage.count()
        self.assertEqual(result, 1)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count_returns_number_of_objects_of_given_class(self):
        """
        Tests that the count() method returns the number of objects
        of the given class in the database.
        """
        state = State(name="California")
        user = User(email="test@example.com", password="password")
        storage.new(state)
        storage.new(user)
        storage.save()
        result = storage.count(State)
        self.assertEqual(result, 1)
        result = storage.count(User)
        self.assertEqual(result, 1)
