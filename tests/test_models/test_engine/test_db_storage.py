#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

import json
import os
import pep8
import unittest
import inspect
import models
from unittest.mock import patch, Mock
from datetime import datetime
from models.engine import db_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
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

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    @patch.object(models.storage, 'all')
    def test_get(self, mock_all):
        """Test that get retrieve one object"""
        mock_user = Mock(spec=classes.get('State'))
        mock_user.id = '1234567890'
        cls = mock_user.__class__

        # All returns a dictionary containing object
        mock_all.return_value = {f'{cls.__name__}.{mock_user.id}': mock_user}
        obj = models.storage.get(cls, mock_user.id)
        mock_all.assert_called_once_with(cls)
        # Test that the object returned matches with the expected object
        self.assertEqual(mock_user, obj)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    @patch.object(models.storage, 'all')
    def test_count_cls_not_none(self, mock_all):
        """
        Test that count returns 1 when a class and ID are passed.
        This is with 1 total object in the database of type Place.
        """
        mock_place = Mock(spec=classes.get('Place'))
        mock_place.id = '1234567890'
        cls = mock_place.__class__

        # All returns a dictionary containing a single Place object
        mock_all.return_value = {f'{cls.__name__}.{mock_place.id}': mock_place}

        count = models.storage.count(cls)
        mock_all.assert_called_once_with(cls)

        self.assertEqual(count, 1)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    @patch.object(models.storage, 'all')
    def test_count_cls_none(self, mock_all):
        """
        Test that count returns 2 when None or an empty class is passed.
        This is with 2 total objects in the database of type Place and State.
        """
        mock_place = Mock(spec=classes.get('Place'))
        mock_state = Mock(spec=classes.get('State'))

        mock_place.id = '1234567890'
        mock_state.id = '0987654321'

        place_cls = mock_place.__class__
        state_cls = mock_state.__class__

        # All returns a dictionary containing a Place and State object
        mock_all.return_value = {
            f'{place_cls.__name__}.{mock_place.id}': mock_place,
            f'{state_cls.__name__}.{mock_state.id}': mock_state
        }
        count = models.storage.count(None)
        mock_all.assert_called_once_with(None)

        self.assertEqual(count, 2)
