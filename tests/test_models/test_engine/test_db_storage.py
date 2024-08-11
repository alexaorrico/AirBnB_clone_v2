#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
import models
from models import storage
from models.engine import db_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from console import HBNBCommand
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import sys
from io import StringIO
import json
import os
import pycodestyle
import unittest
DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}

db = os.getenv("HBNB_TYPE_STORAGE")


@unittest.skipIf(db != 'db', "Testing DBStorage onl")
class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pycodestyle_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pycode = pycodestyle.StyleGuide(quiet=True)
        result = pycode.check_files(['models/engine/db_storage.py'])
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


@unittest.skipIf(db != 'db', "Testing DBStorage only")
class TestDBStorage(unittest.TestCase):
    """Test the DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """ Initialising all the classess"""
        cls.dbstorage = DBStorage()
        cls.output = StringIO()
        sys.stdout = cls.output

    @classmethod
    def teardownClass(cls):
        """ deletes all variables """
        del cls.dbstorage
        del cls.output

    def create(self):
        """returns the console prompt """
        return HBNBCommand()

    def test_new(self):
        """ testing the new class created """
        new_obj = State(name="Carlifornia")
        self.assertEqual(new_obj.name, "Carlifornia")

    def test_dbstorage_attr(self):
        """ Testing user attributes """
        usr = User(email="theeapedo@gmail.com", password="qwerty")
        self.assertTrue(usr.email, "theeapedo@gmail.com")
        self.assertTrue(usr.password, "qwerty")

    def test_dbstorage_get(self):

        """ Testing get method """
        new_state = State(name="Nebraska")
        storage.new(new_state)
        key = f"State.{new_state.id}"
        res = storage.get("State", new_state.id)
        self.assertTrue(res.id, new_state.id)
        self.assertIsInstance(res, State)

    def test_count(self):
        """ Tests the count method of db_storage"""
        storage.reload()
        pre_count = storage.count("State")
        new_state = State(name="Alabama")
        storage.new(new_state)
        new_state1 = State(name="Newyork")
        storage.new(new_state1)
        new_state2 = State(name="Virginia")
        storage.new(new_state2)
        post_count = storage.count("State")
        self.assertTrue(pre_count < post_count)
