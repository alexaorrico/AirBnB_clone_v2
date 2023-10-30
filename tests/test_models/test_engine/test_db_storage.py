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
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.state import State
from models.base_model import Base, BaseModel

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
    """Test the DBStorage class"""
    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', "not testing db storage")
    def test_all(self):
        """Test that all returns the list of all objects"""
        storage = DBStorage()
        all_objs = storage.all()
        self.assertIsNot(all_objs, None, "all() must return a dict")
        self.assertEqual(type(all_objs), dict, "all() must return a dict")

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', "not testing db storage")
    def test_new(self):
        """Test that new adds an object to the database"""
        storage = DBStorage()
        new_state = State(name="California")
        new_state.save()
        all_objs = storage.all(State)
        self.assertTrue(all_objs[new_state.id] == new_state, "State not added to database")

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to the database"""
        storage = DBStorage()
        new_state = State(name="Nevada")
        new_state.save()
        storage.save()
        Session = sessionmaker(bind=storage._DBStorage__engine)
        session = Session()
        result = session.query(State).filter_by(name="Nevada").first()
        self.assertIsNot(result, None, "State not saved to database")

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', "not testing db storage")
    def test_get(self):
        """Test that get retrieves an object by class and ID"""
        storage = DBStorage()
        new_state = State(name="California")
        new_state.save()
        retrieved_state = storage.get(State, new_state.id)
        self.assertEqual(retrieved_state, new_state, "State not retrieved correctly")

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', "not testing db storage")
    def test_count(self):
        """Test that count returns the correct count of objects in storage"""
        storage = DBStorage()
        state_count = storage.count(State)
        new_state = State(name="Texas")
        new_state.save()
        updated_state_count = storage.count(State)
        self.assertEqual(updated_state_count, state_count + 1, "Count not updated correctly")

if __name__ == "__main__":
    unittest.main()
