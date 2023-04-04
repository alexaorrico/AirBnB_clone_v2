#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
from io import StringIO
from unittest.mock import patch
import models
from models.engine import db_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage
from models import FileStorage
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

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pcs = pycodestyle.StyleGuide(quiet=True)
        result = pcs.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pcs = pycodestyle.StyleGuide(quiet=True)
        result = pcs.check_files(['tests/test_models/test_engine/\
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


@unittest.skipIf(type(models.storage) == FileStorage, "Testing FileStorage")
class TestStateDBInstances(unittest.TestCase):
    """DBStorage State Tests"""
    def tearDown(self):
        """Remove storage objs"""
        storage.drop_table(State)

    def setUp(self):
        """Initializes new BaseModel obj"""
        self.state_obj1 = State(name='OK')
        self.state_obj1.save()
        self.state_obj2 = State(name='AR')
        self.state_obj2.save()
        storage.save()
        storage.reload()

    def test_count_meth(self):
        """tests count method for DBStorage"""
        total_states = storage.count(State)
        self.assertEqual(total_states, 2)

    def test_get_meth(self):
        """tests get method for DBStorage"""
        oklahoma_get = storage.get(State, self.state_obj1.id)
        self.assertEqual(oklahoma_get.name, 'OK')

    def test_get_existing_object(self):
        self.assertEqual(storage.get(State,
                                     self.state_obj1.id), self.state_obj1)

    def test_get_non_existing_object(self):
        self.assertIsNone(storage.get(State, 'invalid_id'))

    def test_count_all_objects(self):
        self.assertEqual(storage.count(), 2)

    def test_count_objects_of_class(self):
        self.assertEqual(storage.count(State), 2)


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""
    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(models.storage.all()), dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""
        with patch('sys.stdout', new=StringIO()) as f:
            command = 'all'
            classes().onecmd(command)
            output = f.getvalue().strip()
            self.assertTrue(len(output) > 0)

            # Verify that all objects are in output
            for class_name, class_obj in classes.items():
                for obj in storage.all(class_obj).values():
                    self.assertIn(obj.__str__(), output)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """test that new adds an object to the database"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""
