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
import os
import pep8
import MySQLdb
import unittest
from unittest import mock


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
        result = pep8s.check_files(
            ['tests/test_models/test_engine/test_db_storage.py']
        )
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


@unittest.skipIf(models.storage_t != 'db', "not testing db storage")
class TestDBStorage(unittest.TestCase):
    """Test the FileStorage class"""
    @mock.patch('models.engine.db_storage.create_engine')
    def test_engine_creation_on_init(self, mocked_create_engine):
        """Test engine creation when the storage instane is created"""
        storage = models.engine.db_storage.DBStorage()
        HBNB_MYSQL_USER = os.getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = os.getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = os.getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = os.getenv('HBNB_MYSQL_DB')

        create_engine_args = 'mysql+mysqldb://{}:{}@{}/{}'.format(
            HBNB_MYSQL_USER,
            HBNB_MYSQL_PWD,
            HBNB_MYSQL_HOST,
            HBNB_MYSQL_DB)

        self.assertTrue(mocked_create_engine.called)
        mocked_create_engine.assert_called_with(create_engine_args,
                                                pool_pre_ping=True)
        del storage

    @mock.patch('models.engine.db_storage.Base.metadata.drop_all')
    def test_tables_drop_in_testdev(self, mocked_drop_all):
        """Test tables drop if the current env is a test env"""
        storage = models.engine.db_storage.DBStorage()
        self.assertTrue(mocked_drop_all.called)
        del storage

    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(models.storage.all()), dict)

    def test_all_with_class(self):
        """Test that all returns all rows when no class is passed"""
        state = State()
        state.name = "Kh"
        state.save()
        states_old = models.storage.all(State)
        models.storage.close()
        state = State()
        state.name = "JZ"
        state.save()
        models.storage.close()
        states_new = models.storage.all(State)

        self.assertTrue(len(states_old) <= len(states_new))

    def test_new(self):
        """test that new adds an object to the database"""

    def test_save(self):
        """Test that save properly saves objects to file.json"""

    def test_get_methods(self):
        """Test DBStorage.get based on the class and id
           Normal case"""
        state = State()
        state.name = "Khartoum"
        state.save()
        get_state = models.storage.get(State, state.id)
        self.assertIsInstance(get_state, State)
        self.assertEqual(state.id, get_state.id)
        self.assertEqual(state.name, get_state.name)

    def test_get_no_inst(self):
        """Test DBStorage.get based on the class and id
        No id matched
        """
        get_state = models.storage.get(State, "1234567")
        self.assertTrue(get_state is None)

    def test_get_none_class(self):
        """Test DBStorage.get based on the class and id
        provide cls as None
        """
        get_state = models.storage.get(None, "1234567")
        self.assertTrue(get_state is None)

    def test_acount_method(self):
        """Test DBStorage.count
        """
        state = State()
        state.name = "Khartoum"
        state.save()
        for i in range(3):
            city = City()
            city.name = f"Khartoum{i}"
            city.state_id = state.id
            city.save()
        models.storage.close()
        all_db_instances = models.storage.count()
        state_db_instances = models.storage.count(State)
        city_db_instances = models.storage.count(City)

        self.assertEqual(all_db_instances, 4)
        self.assertEqual(state_db_instances, 1)
        self.assertEqual(city_db_instances, 3)

    def test_acount_method_wrong_cls(self):
        """Test DBStorage.count with wrong class"""
        db_instances = models.storage.count("City")
        self.assertEqual(db_instances, 0)
