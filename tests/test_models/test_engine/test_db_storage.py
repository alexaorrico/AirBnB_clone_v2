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
from unittest.mock import patch
DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        cls.storage = DBStorage()
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
                            "{:s} method ineeds a docstring".format(func[0]))

    def test_count_empty(self):
        """tests for method count when empty"""
        self.assertEqual(self.storage.count(), 0)

    def test_count_after_creating(self):
        """tests for method count"""
        storage = DBStorage()

        self.storage.new(State(name='California'))
        self.storage.new(State(name='Ohio'))
        self.assertEqual(self.storage.count(), 2)

    def test_count_nonexistent_class(self):
        """test for count when we parse a nonexistent class"""
        with self.assertRaises(ValueError):
            self.storage.count(NonExistentClass)

    def test_count_after_deleting(self):
        """test for count number after deleting"""
        self.storage.new(State(name='Nevada'))
        self.storage.new(State(name='Miami'))
        self.storage.delete(State, 'Miami')
        self.assertEqual(self.storage.count(), 1)
        self.storage.delete(State, 'Nevada')
        self.assertEqual(self.storage.count(), 0)

    def test_count_after_reloading(self):
        """test after reloading storage"""
        self.storage.new(State(name='Illinois'))
        self.storage.reload()
        self.assertEqual(self.storage.count(), 1)

    @patch('storage.DBStorage.__session')
    def test_get_found_obj(self, mock_session):
        """method that tests if get method retrieves one object
        and the object exists"""
        mock_query = mock_session.query.return_value
        mock_query.first.return_value = State(id="234", name='Ohio')

        storage = DBStorage()
        state = storage.get(State, "234")

        # Assertions
        self.assertEqual(state.id, '234')
        self.assertEqual(state.name, 'Ohio')
        mock_query.assert_called_once_with(State)
        mock_query.filter.assert_called_once_with(State.id == '234')

    @patch('storage.DBStorage.__session')
    def test_get_notfound_obj(self, mock_session):
        """test when the object is not found"""
        mock_query = mock_session.query.return_value.filter.return_value
        mock_query.first.return_value = None

        storage = DBStorage()
        state = storage.get(State, '567')

        # Assertions
        self.assertIsNone(state)
        mock_session.query.assert_called_once_with(State)
        mock_session.filter.assert_called_once_with(State.id == '567')
        mock_query.first.assert_called_once()

#    def test_get_method(self):
#        """tests the get method returns the required value"""
#        self.assertEqual(DBStorage.get(User, "1234"), self.user1)
#        self.assertIsNone(DBStorage.get(User, "5789"))


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

    def test_get(self):
        """Test that tests the get method"""
