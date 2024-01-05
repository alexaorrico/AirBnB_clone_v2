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
    ##
    def setUp(self):
        # Set up a temporary test file
        self.test_file_path = 'test_storage.json'
        self.storage = FileStorage()
        self.storage._FileStorage__file_path = self.test_file_path

    def tearDown(self):
        # Clean up: remove the temporary test file if it exists
        if os.path.exists(self.test_file_path):
            os.remove(self.test_file_path)

    def test_reload_method(self):
        # Test reloading from a non-existent file
        self.storage.reload()
        self.assertEqual(len(self.storage.all()), 0)

        # Test reloading from an existing file with valid data
        data = {'obj1': {'__class__': 'SomeClass', 'attr1': 'value1'}}
        with open(self.test_file_path, 'w') as f:
            json.dump(data, f)
        self.storage.reload()
        self.assertEqual(len(self.storage.all()), 1)

        # Test reloading from a file with invalid JSON data
        with open(self.test_file_path, 'w') as f:
            f.write('invalid_json_data')
        self.storage.reload()
        self.assertEqual(len(self.storage.all()), 0)

    def test_get_method(self):
        # Test the get method with some sample data
        data = {'obj1': {'__class__': 'SomeClass', 'attr1': 'value1'}}
        with open(self.test_file_path, 'w') as f:
            json.dump(data, f)

        # Ensure the object is retrieved
        obj = self.storage.get('SomeClass', 'obj1')
        self.assertIsNotNone(obj)

        # Test with non-existent class and object ID
        non_existent_obj = self.storage.get('NonExistentClass', 'non_existent_obj')
        self.assertIsNone(non_existent_obj)

    def test_count_method(self):
        # Test the count method with some sample data
        data = {'obj1': {'__class__': 'SomeClass', 'attr1': 'value1'}}
        with open(self.test_file_path, 'w') as f:
            json.dump(data, f)

        # Ensure the count is correct
        count_all = self.storage.count()
        self.assertEqual(count_all, 1)

        # Test count with a specific class
        count_some_class = self.storage.count('SomeClass')
        self.assertEqual(count_some_class, 1)

        # Test count with a non-existent class
        count_non_existent_class = self.storage.count('NonExistentClass')
        self.assertEqual(count_non_existent_class, 0)


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
