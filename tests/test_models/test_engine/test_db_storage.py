#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

# from datetime import datetime
import inspect
import models
from models.engine import db_storage
from models.amenity import Amenity
# from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
# import json
# import os
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


class TestDbStorage(unittest.TestCase):
    """Testing DB_Storage class"""
    def test_get(self):
        """Test get returns object of class & Id passed"""
        s1 = State(name="Abuja")
        models.storage.new(s1)
        result = models.storage.get(State, s1.id)
        self.assertEqual(result.id, s1.id)
        self.assertIsInstance(result, State)

    def test_count(self):
        """Test count returns the right number of objects"""
        dict1 = models.storage.all()
        count1 = models.storage.count()
        self.assertEqual(len(dict1), count1)
        dict2 = models.storage.all(State)
        count2 = models.storage.count(State)
        self.assertEqual(len(dict2), count2)


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
        """Test that get returns the object based on the class and id"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count_returns_all_objs_number(self):
        """Test that count returns the total number
        of all objects in storage"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count_returns_objs_number(self):
        """Test that count returns the total number of objects in storage"""
