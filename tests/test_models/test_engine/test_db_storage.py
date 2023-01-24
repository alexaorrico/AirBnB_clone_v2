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
from os import getenv
from models.base_model import Base
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
    """Test the DBStorage class"""

    @unittest.skipIf(models.storage_t != 'db', "not testing file storage")
    @classmethod
    def setUpClass(cls):
        """Setup a classwide test fixture.
        Deletes all records of all classes"""
        for clss in classes.values():
            models.storage._DBStorage__session.query(clss).delete()

    @unittest.skipIf(models.storage_t != 'db', "not testing file storage")
    def setUp(self):
        """Set up test environment"""
        self.state_1 = State(name="Mombasa")
        self.state_2 = State(name="Nairobi")
        self.amenity_1 = Amenity(name="wifi")
        models.storage.new(self.amenity_1)
        models.storage.new(self.state_1)
        models.storage.new(self.state_2)
        models.storage.save()

    @unittest.skipIf(models.storage_t != 'db', "not testing file storage")
    def tearDown(self):
        """Clean up after a test"""
        models.storage.delete(self.state_1)
        models.storage.delete(self.state_2)
        models.storage.delete(self.amenity_1)
        models.storage.save()

    @unittest.skipIf(models.storage_t != 'db', "not testing file storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(models.storage.all()), dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing file storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""
        self.assertEqual(len(models.storage.all()), 3)

    @unittest.skipIf(models.storage_t != 'db', "not testing file storage")
    def test_all_with_class(self):
        """Test that all returns all of a specific class when no class is
        passed"""
        self.assertEqual(len(models.storage.all(State)), 2)

    @unittest.skipIf(models.storage_t != 'db', "not testing file storage")
    def test_new(self):
        """test that new adds an object to the session"""
        new_state = State(name="Atlantis")
        models.storage.new(new_state)
        models.storage._DBStorage__session.commit()
        retrieved_state = models.storage._DBStorage__session.query(State)\
            .filter_by(id=new_state.id).one()
        self.assertIs(retrieved_state, new_state)
        models.storage.delete(new_state)
        models.storage.save()

    @unittest.skipIf(models.storage_t != 'db', "not testing file storage")
    def test_save(self):
        """Test that save properly saves objects to the database"""
        amenity = Amenity(name="swimming_pool")
        models.storage.new(amenity)
        models.storage.save()
        retrieved_amenity = models.storage._DBStorage__session.query(Amenity)\
            .filter_by(id=amenity.id).one()
        self.assertIs(amenity, retrieved_amenity)
        models.storage.delete(amenity)
        models.storage.save()

    @unittest.skipIf(models.storage_t != 'db', "not testing file storage")
    def test_get_with_correct_id_and_class(self):
        """Test that get returns correct object based on class and id"""
        retreived_state = models.storage.get(self.state_1.__class__,
                                             self.state_1.id)
        self.assertIsInstance(retreived_state, State)
        self.assertIs(retreived_state, self.state_1)

    @unittest.skipIf(models.storage_t != 'db', "not testing file storage")
    def test_get_with_invalid_class_or_id(self):
        """Test that get will return None when passed invalid input"""
        retrieved_state = models.storage.get(None, None)
        self.assertIsNone(retrieved_state, "invalid class or id was passed")
        retrieved_state = models.storage.get(State, 'fake_id')
        self.assertIsNone(retrieved_state, "invalid class or id was passed")

    @unittest.skipIf(models.storage_t != 'db', "not testing file storage")
    def test_count_with_class(self):
        """Test that count returns correct number of objects of a particular
        class"""
        total = models.storage.count(State)
        self.assertIsInstance(total, int)
        self.assertEqual(total, 2)

    @unittest.skipIf(models.storage_t != 'db', "not testing file storage")
    def test_count_without_class(self):
        """Testing that count returns correct number of total objects in
        storage"""
        total = models.storage.count()
        self.assertIsInstance(total, int)
        self.assertEqual(total, 3)
