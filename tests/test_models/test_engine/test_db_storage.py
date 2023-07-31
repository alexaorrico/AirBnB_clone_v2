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

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get(self):
        """Test that the get properly gets objects"""
        obj = State(name="Test")
        obj.save()
        got_obj = models.storage.get('State', obj.id)
        self.assertIs(obj, got_obj)

        obj.delete()

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get_fail(self):
        """Test that the get properly gets objects"""
        obj = State(name="Test")
        obj.save()
        got_obj = models.storage.get('ls', obj.id)
        self.assertIsNot(obj, got_obj)

        obj.delete()

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count(self):
        """Test that the count properly counts objects"""
        got_obj_count = models.storage.count()
        obj_count = len(models.storage.all())
        self.assertEqual(got_obj_count, obj_count)

        got_obj_count = models.storage.count('State')
        obj_count = len(models.storage.all('State'))
        self.assertEqual(got_obj_count, obj_count)

    def test_count_too_many_args(self):
        """Tests failure when too many args"""
        with self.assertRaises(TypeError):
            models.storage.count("1", "2")

    def test_count_none(self):
        """Test that count properly counts objects"""
        self.assertFalse(models.storage.count("NotAClass"))

    def test_count_bad_type(self):
        """Test that count properly counts when given wrong type"""
        self.assertFalse(models.storage.count({'hi': 'bye'}))

    def test_get_type_id(self):
        """tests get when type of id is wrong"""
        self.assertEqual(models.storage.get("State", []), None)

    def test_get_no_class(self):
        """tests get when cls does not exist"""
        self.assertEqual(models.storage.get("NotAClass", "11111"), None)

    def test_get_no_id(self):
        """tests get when id does not exist"""
        self.assertEqual(models.storage.get("State", "1111"), None)
