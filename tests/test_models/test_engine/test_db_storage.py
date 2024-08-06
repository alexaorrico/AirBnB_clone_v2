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


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""
    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(models.storage.all()), dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""
        state_data = {"name": "Khartoum"}
        new_state = State(**state_data)
        models.storage.new(new_state)
        models.storage.save()

        session = models.storage._DBStorage__session

        all_obj = session.query(State).all()
        self.assertTrue(len(all_obj) > 0)


    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """test that new adds an object to the database"""
        state_data = {"name": "lagos"}
        new_state = State(**state_data)
        models.storage.new(new_state)

        session = models.storage._DBStorage__session
        retrieve_state = session.query(State).filter_by(id=new_state).first()

        self.assertEqual(retrieve_state.id, new_state.id)
        self.assertEqual(retrieve_state.name, new_state.name)
        self.assertIsNone(retrieve_state)
    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""
        state_data = {"name": "Nirobi"}
        new_state = State(**state_data)
        models.storage.save()

        session = models.storage._DBStorage__session
        retrieve_state = session.query(State).filter_by(id=new_state).first()

        self.assertEqual(retrieve_state.id, new_state.id)
        self.assertEqual(retrieve_state.name, new_state.name)
        self.assertIsNone(retrieve_state)
    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get(self):
        """Tests if the get method works as intended"""
        self.state = State(name="Texas")
        self.state.save()
        self.assertTrue(models.storage.get("State", self.state.id))

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count(self):
        """Tests if the count method works as intended"""
        cls_count_start = models.storage.count()
        self.state = State(name="Texas")
        models.storage.new(self.state)
        self.state.save()
        cls_count_finish = models.storage.count()
        self.assertNotEqual(cls_count_start, cls_count_finish)
    """
    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def get(self, cls, id):
        storage = models.storage
        storage.reload()
        state_data = {"name": "Bali"}
        state_inst = State(**state_data)
        storage.new(state_inst)
        storage.save()

        retreve_state = storage.get(State, state_inst.id)

        self.assertEqual(state_inst, retreve_state)

        fake_state_id = storage.get(State, 'fake_id')

        self.assertEqual(fake_state_id, None)
    
    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def count(self, cls=None):
        storage = models.storage
        storage.reload()
        state_data = {"name": "Kenya"}
        state_inst = State(**state_data)
        storage.new(state_inst)

        city_data = {"name": "Paris", "state_id": state_inst.id}
        city_inst = City(**city_data)
        storage.new(city_inst)
        storage.save()

        state_occur = storage.count(State)
        self.assertEqual(state_occur, len(storage.all(State)))

        state_occur = storage.count()
        self.assertEqual(state_occur, len(storage.all()))
        """




        




