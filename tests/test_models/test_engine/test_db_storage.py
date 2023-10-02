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
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import json
from os import getenv
import pep8
import unittest
DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


@unittest.skipIf(models.storage_t != 'db', "not testing db storage")
class TestDBStorage(unittest.TestCase):
    """Test the DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up the test environment"""
        cls.db_engine = create_engine('sqlite:///:memory:')
        cls.Session = sessionmaker(bind=cls.db_engine)
        cls.db_session = cls.Session()
        Base.metadata.create_all(bind=cls.db_engine)
        cls.storage = DBStorage()
        cls.storage.reload()

    @classmethod
    def tearDownClass(cls):
        """Clean up the test environment"""
        cls.db_session.close()
        Base.metadata.drop_all(bind=cls.db_engine)

    def setUp(self):
        """Start a new transaction for each test"""
        self.transaction = self.db_session.begin_nested()
        self.storage.reload()

    def tearDown(self):
        """Roll back the transaction after each test"""
        self.transaction.rollback()

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionary"""
        self.assertIs(type(models.storage.all()), dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """Test that new adds an object to the database"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to database"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get(self):
        """Test that get method retrieves an object from the database"""
        state = State(name="California")

        # Save state object to db
        models.storage.new(state)
        models.storage.save()

        # Get object from the db
        retrieved_state = models.storage.get(State, state.id)
        self.assertEqual(state, retrieved_state)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count(self):
        """Test that count method returns total number of objects in db"""
        state = State(name="California")
        city1 = City(name="New York", state_id=state.id)
        city2 = City(name="Miami", state_id=state.id)

        # Save the objects to the database
        models.storage.new(state)
        models.storage.new(city1)
        models.storage.new(city2)
        models.storage.save()

        # Get City object count in the db
        city_count = models.storage.count(City)
        self.assertEqual(city_count, 2)

        # Get total object count in the db
        total_count = models.storage.count()
        self.assertEqual(total_count, len(models.storage.all()))


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
