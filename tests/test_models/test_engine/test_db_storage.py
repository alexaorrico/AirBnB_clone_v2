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
import pycodestyle
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

    def test_pycodestyle_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pycodestyles = pycodestyle.StyleGuide(quiet=True)
        result = pycodestyles.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pycodestyle_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pycodestyles = pycodestyle.StyleGuide(quiet=True)
        result = pycodestyles.check_files(['tests/test_models/test_engine/\
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
    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(models.storage.all()), dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""
        state = State(name="California")
        state.save()
        self.assertEqual(models.storage.all(), models.storage.all(State))

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """test that new adds an object to the database"""
        state = State(name="California")
        state.save()
        self.assertIn(state, models.storage.all().values())

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""
        state = State(name="California")
        state.save()
        models.storage.reload()
        self.assertIn("State.{}".format(state.id), models.storage.all().keys())

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count(self):
        """Test that count returns the number of objects in storage"""
        state = State(name="California")
        state.save()
        self.assertEqual(models.storage.count(State), 1)
        self.assertEqual(models.storage.count(), 1)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get(self):
        """Test that get returns the object based on the class and id"""
        state = State(name="California")
        self.assertEqual(models.storage(State, state.id), state)


class TestDBStorageMethodsGet(unittest.TestCase):
    """
    Class for Test File Storage Methods Get and count
    """
    @classmethod
    def setUpClass(cls):
        """
        setup tests for class
        """
        print('...... Testing Get() Method ......')

    def setUp(self):
        """
        Set up
        """
        self.storage = DBStorage()
        self.state_obj = State(id=1812)
        self.storage.new(self.state_obj)
        self.storage.save()

    def tearDown(self):
        """
        Clean up after each test
        """
    @unittest.skipIf(models.storage_t != 'db', "not testing file storage")
    def test_get_1(self):
        """Get function"""
        self.assertEqual(self.storage.get(State, 1812), self.state_obj)

    @unittest.skipIf(models.storage_t != 'db', "not testing file storage")
    def test_get_nonexistent(self):
        """Get function"""
        self.assertEqual(self.storage.get(State, 153), None)

    @unittest.skipIf(models.storage_t != 'db', "not testing file storage")
    def test_get_2(self):
        """Get function"""
        self.assertEqual(self.storage.get(State, 153), None)

    @unittest.skipIf(models.storage_t != 'db', "not testing file storage")
    def test_get_invalid_cls(self):
        """Get function"""
        self.assertEqual(self.storage.get(None, 153), None)


class TestStorageCount(unittest.TestCase):
    """Count function"""
    @classmethod
    def setUpClass(cls):
        """
        setup tests for class
        """
        print('...... Testing Count() Method ......')

    def setup(self):
        """
        setup method
        """
        self.storage = DBStorage()
        self.state1 = State(name="California")
        self.state1.save()
        self.state2 = State(name="Colorado")
        self.state2.save()
        self.state3 = State(name="Wyoming")
        self.state3.save()
        self.state4 = State(name="Virgina")
        self.state4.save()
        self.state5 = State(name="Oregon")
        self.state5.save()
        self.state6 = State(name="New_York")
        self.state6.save()
        self.state7 = State(name="Ohio")
        self.state7.save()

    @unittest.skipIf(models.storage_t != 'db', "not testing file storage")
    def test_count_all(self):
        """test  count all states"""
        expected_count = len(self.storage.all())
        self.assertEqual(self.storage.count(), expected_count)

    @unittest.skipIf(models.storage_t != 'db', "not testing file storage")
    def test_count_cls(self):
        """
        test count with specific  class
        """
        expected_count = len(self.storage.all(State))
        self.assertEqual(self.storage.count(State), expected_count)

    @unittest.skipIf(models.storage_t != 'db', "not testing file storage")
    def test_count_all_empty(self):
        """
        Test count with no class specified and storage is empty
        """
        self.storage.all().clear()
        self.assertEqual(self.storage.count(), 0)

    @unittest.skipIf(models.storage_t != 'db', "not testing file storage")
    def test_count_cls_empty(self):
        """
        Test count with a specific class and storage is empty
        """
        self.storage.all().clear()
        self.assertEqual(self.storage.count(State), 0)

class TestDBStorageGetCount(unittest.TestCase):
    def setUp(self):
        self.storage = DBStorage()
        self.place = Place()
        self.review = Review()
        self.user = User()

    @unittest.skipIf(models.storage_t != 'db', "not testing file storage")
    def test_get_with_db_storage(self):
        result = self.storage.get(Place, "some_id")
        expected_msg = "OK"
        self.assertEqual(result, expected_msg, msg=f"Got {result}, expected {expected_msg}")

    @unittest.skipIf(models.storage_t != 'db', "not testing file storage")
    def test_count_with_db_storage(self):
        result = self.storage.count(Place)
        expected_msg = "OK"
        self.assertEqual(result, expected_msg, msg=f"Got {result}, expected {expected_msg}")

if __name__ == '__main__':
    unittest.main()
