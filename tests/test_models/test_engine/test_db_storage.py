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


class TestDBStorage(unittest.TestCase):
    """Test the FileStorage class"""
    def setUp(self):
        """Set up before test"""
        pass

    def tearDown(self):
        """Close after test"""
        pass

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(models.storage.all()), dict)
        test = models.storage.all()
        print(test)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""
        new_dict = models.storage.all()
        for k, v in new_dict.items():
            self.assertEqual(type(v) in classes.values(), True)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """test that new adds an object to the database"""
        test = State(name="TEST")
        models.storage.new(test)
        models.storage.save()
        dic = models.storage.all(State)
        bool = False
        for obj in dic.values():
            if obj.name == "TEST":
                bool = True
        self.assertEqual(bool, True)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""
        test = State(name="TEST")
        models.storage.new(test)
        models.storage.save()
        dic = models.storage.all(State)
        bool = False
        for obj in dic.values():
            if obj.name == "TEST":
                bool = True
        self.assertEqual(bool, True)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_reload(self):
        """Test that reload properly reload objects to __objects"""
        models.storage.reload()

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_delete(self):
        """Test if objs will delete when delete method is called"""
        test = State(name="Test")
        models.storage.new(test)
        models.storage.save()
        dic = models.storage.all(State)
        bool = False
        for obj in dic.values():
            if obj.id == test.id:
                models.storage.delete(obj)
                models.storage.save()
                bool = True
        dic = models.storage.all(State)
        for obj in dic.values():
            if obj.id == test.id:
                bool = False
        self.assertEqual(bool, True)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_close(self):
        """Test close"""
        models.storage.reload()
        models.storage.close()

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get(self):
        """test get function"""
        from models import storage
        test = State(name="TEST")
        storage.new(test)
        storage.save()
        first_state_id = list(models.storage.all("State").values())[0].id
        obj = models.storage.get("State", first_state_id)
        self.assertTrue(obj.__class__.__name__, "State")
        self.assertTrue(obj.id, first_state_id)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count(self):
        """test count function"""
        count_state = models.storage.count("State")
        count_city = models.storage.count("City")
        count_place = models.storage.count("Place")
        count_review = models.storage.count("Review")
        count_user = models.storage.count("User")
        count_am = models.storage.count("Amenity")
        count = models.storage.count()
        self.assertTrue(count >= count_state, True)
        self.assertTrue(count >= count_city, True)
        self.assertTrue(count >= count_place, True)
        self.assertTrue(count >= count_review, True)
        self.assertTrue(count >= count_user, True)
        self.assertTrue(count >= count_am, True)
