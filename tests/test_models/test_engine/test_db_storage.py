#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
import models
from models.engine import db_storage
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import pep8
import unittest
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
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

    def setUp(self):
        """set up our database for testing"""
        # Create an in-memory SQLite database for testing
        self.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        self.test_db_storage = DBStorage()
        self.test_db_storage._DBStorage__session = self.session

    def tearDown(self):
        """Tear down the test envirenment"""
        self.session.close_all()
        Base.metadata.drop_all(self.engine)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        # Create some test objects
        amenity1 = Amenity(name='Swimming Pool')
        amenity2 = Amenity(name='Gym')
        self.test_db_storage.new(amenity1)
        self.test_db_storage.new(amenity2)
        self.test_db_storage.save()

        self.assertIs(type(models.storage.all()), dict)

        # Call the all() method with Amenity class
        result = self.test_db_storage.all(cls=Amenity)
        # Check if the result is a dictionary and contains the expected objects
        self.assertIsInstance(result, dict)
        self.assertIn('Amenity.' + amenity1.id, result)
        self.assertIn('Amenity.' + amenity2.id, result)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """test that new adds an object to the database"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get(self):
        """Test that get method gets the apropriate object for the id"""
        s = State(name="Alabama")
        self.test_db_storage.new(s)
        s_get = self.test_db_storage.get(State, s.id)

        self.assertIsInstance(s_get, State)
        self.assertEqual(s, s_get)
        self.assertEqual(s.id, s_get.id)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get_invalide(self):
        """Test the invalide cases of get method"""
        s = State(name="Alabama")
        s_get = self.test_db_storage.get(None, s.id)
        self.assertIsNone(s_get)
        s_get = self.test_db_storage.get(State, None)
        self.assertIsNone(s_get)
        s_get = self.test_db_storage.get(State, "")
        self.assertIsNone(s_get)
        s_get = self.test_db_storage.get(State, "invalide_id")
        self.assertIsNone(s_get)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count(self):
        """the count method to get the number of objects or all objects"""
        count = self.test_db_storage.count()

        count1 = self.test_db_storage.count(State)
        s = State(name="Alabama")
        self.test_db_storage.new(s)
        count2 = self.test_db_storage.count(State)

        self.assertEqual(count + 1, len(self.test_db_storage.all()))
        self.assertEqual(count1 + 1, count2)
