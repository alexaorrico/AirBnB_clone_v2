#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
import models
from models import storage, storage_t
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


@unittest.skipIf(storage_t != 'db', "not testing db storage")
class TestDBStorage(unittest.TestCase):
    """Test the DBStorage class"""
    @unittest.skipIf(storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionary"""
        self.assertIs(type(storage.all()), dict)

    @unittest.skipIf(storage_t != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""
        all_objs = storage.all()
        self.assertIsInstance(all_objs, dict)
        self.assertGreaterEqual(len(all_objs), 0)

    @unittest.skipIf(storage_t != 'db', "not testing db storage")
    def test_all_with_class(self):
        """Test that all returns correct type when class is passed"""
        all_states = storage.all(State)
        self.assertIsInstance(all_states, dict)
        for obj in all_states.values():
            self.assertIsInstance(obj, State)

    @unittest.skipIf(storage_t != 'db', "not testing db storage")
    def test_new(self):
        """test that new adds an object to the database"""
        new_state = State(name="Texas")
        storage.new(new_state)
        storage.save()
        self.assertIn(new_state, storage.all(State).values())

    @unittest.skipIf(storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""
        new_state = State(name="Nevada")
        storage.new(new_state)
        storage.save()
        saved_state = storage.all(State).get("State." + new_state.id)
        self.assertIsNotNone(saved_state)
        self.assertEqual(saved_state.name, "Nevada")

    @unittest.skipIf(storage_t != 'db', "not testing db storage")
    def test_delete(self):
        """Test that delete removes object from storage"""
        new_state = State(name="Florida")
        storage.new(new_state)
        storage.save()
        storage.delete(new_state)
        storage.save()
        self.assertNotIn(new_state, storage.all(State).values())

    @unittest.skipIf(storage_t != 'db', "not testing db storage")
    def test_reload(self):
        """Test that reload properly reloads objects from the database"""
        storage.reload()
        all_objs = storage.all()
        self.assertIsInstance(all_objs, dict)
        self.assertGreaterEqual(len(all_objs), 0)

    @unittest.skipIf(storage_t != 'db', "not testing db storage")
    def test_close(self):
        """Test that close properly closes the session"""
        # Ensure close method is callable
        self.assertTrue(callable(storage.close))

        # Close the session and assert that __session is None
        storage.close()
        self.assertIsNone(storage._DBStorage__session)

    @unittest.skipIf(storage_t != 'db', "not testing db storage")
    def test_get(self):
        """Test that get retrieves an object based on class and id"""
        state = State(name="California")
        storage.new(state)
        storage.save()
        self.assertEqual(storage.get(State, state.id), state)
        self.assertIsNone(storage.get(State, "non_existent_id"))

    @unittest.skipIf(storage_t != 'db', "not testing db storage")
    def test_count(self):
        """Test that count returns the correct number of objects"""
        initial_count = storage.count()
        state = State(name="California")
        storage.new(state)
        storage.save()
        self.assertEqual(storage.count(), initial_count + 1)
        self.assertEqual(storage.count(State), 1)
        self.assertEqual(storage.count(City), 0)
