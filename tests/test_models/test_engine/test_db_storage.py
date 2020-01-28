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
from models import storage
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

    def test_all_method(self):
        """ Test all method """
        test_dict = storage.all()
        self.assertIsInstance(test_dict, dict)
        self.assertIs(test_dict, storage._FileStorage__objects)

    def test_new(self):
        """ Test new Method """
        basM = State()
        basM.name = "NINGUNALANDIA"
        storage.new(basM)
        storage.save()
        dictTest = storage.all()
        strForm = "{}.{}".format(type(basM).__name__, basM.id)
        self.assertTrue(strForm in dictTest.keys())

    def test_save(self):
        """ Test save method """
        self.assertIsNotNone(storage.save)
        storage.save()
        with open("file.json", 'r') as read:
            lines = read.readlines()

        try:
            os.remove("file.json")
        except BaseException:
            pass

        storage.save()

        with open("file.json", 'r') as read2:
            lines2 = read2.readlines()

        self.assertEqual(lines, lines2)

    def test_reload(self):
        """ Test reload method """
        self.assertIsNotNone(storage.reload)
        try:
            os.remove("file.json")
        except BaseException:
            pass

        with open("file.json", 'w') as write:
            write.write("{}")
        with open("file.json", 'r') as reader:
            for line in reader:
                self.assertEqual(line, "{}")
        self.assertIs(storage.reload(), None)

    def test_all(self):
        """ Test all method """
        dictTest = storage.all()
        self.assertIsInstance(dictTest, dict)
        self.assertIs(dictTest, storage._FileStorage__objects)

    def test_count(self):
        """ Test all method """
        count1 = len(storage.all())
        count2 = storage.count()
        self.assertEqual(count1, count2)

    def test_get(self):
        """ test get
        """
        tmp_dict = {}
        first_state_id = list(storage.all("State").values())[0].id
        for key, value in storage.all("State").items():
            if first_state_id in key:
                tmp_dict = value
        first_state_id = list(storage.all("State").values())[0].id
        self.assertEqual(storage.get("State", first_state_id), tmp_dict)


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""
    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(models.storage.all()), dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""
        pass

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """test that new adds an object to the database"""
        pass

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""
        pass
