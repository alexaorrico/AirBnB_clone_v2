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


class TestDbStorage(unittest.TestCase):
    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def setUp(self):
        """Setup db"""
        pass

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def tearDown(self):
        """Drop db"""
        pass

    """Test the FileStorage class"""
    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(models.storage.all(State)), dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""
        self.assertIs(type(models.storage.all()), dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """test that new adds an object to the database"""
        pass

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""
        pass

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get_retrieve_one_object(self):
        """Test get() retrieves just one object with right id"""
        obj = State()
        obj.name = "Ogun"
        obj.save()
        search_id = obj.id
        class_name = State
        cls_object = models.storage.get(class_name, search_id)
        self.assertTrue(isinstance(obj, class_name))
        self.assertTrue(isinstance(cls_object, class_name))

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get_with_wrong_id_return_none(self):
        """Test get() return none if wrong id or not found"""
        obj = State()
        obj.name = "Ogun"
        obj.save()
        search_id = obj.id
        class_name = State
        cls_object = models.storage.get(class_name,
                                        "ffffffff-ff79-dfdc-rrra-wwdqqqqcdyyc")
        self.assertTrue(cls_object is None)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count_all_objects_if_no_class_passed(self):
        """Test count() returns the count of all objects in storage"""
        obj = State()
        obj.name = "Ogun"
        obj.save()
        all_count = models.storage.count()
        expected_count = 1
        self.assertEqual(all_count, expected_count)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count_objects_with_given_class(self):
        """Test count() returns the number of objects in storage
        matching the given class"""
        obj = State()
        obj.name = "Ogun"
        obj.save()
        cls_count = models.storage.count(State)
        expected_count = 2
        self.assertEqual(cls_count, expected_count)
