#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
import os
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


class Db_Storage(unittest.TestCase):
    """test get a specific obj"""

    def setup():
        """define environmental variables"""
        os.environ['HBNB_ENV'] = "test"
        os.environ['HBNB_MYSQL_USER'] = "hbnb_test"
        os.environ['HBNB_TYPE_STORAGE'] = "db"
        os.environ['HBNB_MYSQL_PWD'] = "hbnb_test_pwd"
        os.environ['HBNB_MYSQL_HOST'] = "localhost"
        os.environ['HBNB_MYSQL_DB'] = "hbnb_test_db"

    def teardown():
        """define environmental variables"""
        os.environ['HBNB_ENV'] = ""
        os.environ['HBNB_MYSQL_USER'] = ""
        os.environ['HBNB_TYPE_STORAGE'] = ""
        os.environ['HBNB_MYSQL_PWD'] = ""
        os.environ['HBNB_MYSQL_HOST'] = ""
        os.environ['HBNB_MYSQL_DB'] = ""

    @unittest.skipIf(models.storage_t != 'db', "testing db storage")
    def test_get_obj_none(self):
        """check if obj is none"""
        self.assertEqual(None, models.storage.get("Tupac", 44))

    @unittest.skipIf(models.storage_t != 'db', "testing db storage")
    def test_get_obj(self):
        """pass in existing obj"""
        example_state = State(name="rip")
        models.storage.new(example_state)
        models.storage.save()
        id = example_state.id
        self.assertEqual(id, models.storage.get("State", id).id)

    @unittest.skipIf(models.storage_t != 'db', "testing db storage")
    def test_get_count(self):
        """count existing obj"""

        Base.metadata.drop_all(models.storage._DBStorage__engine)
        Base.metadata.create_all(models.storage._DBStorage__engine)
        models.storage.close()

        example_state1 = State(name="notorious")
        models.storage.new(example_state1)
        example_state2 = State(name="50_cent")
        models.storage.new(example_state2)
        id = example_state2.id
        example_city1 = City(state_id=id, name="zurich")
        models.storage.new(example_city1)
        models.storage.save()
        self.assertEqual(3, models.storage.count())
        self.assertEqual(2, models.storage.count("State"))


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""
    @unittest.skipIf(models.storage_t == 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(models.storage.all()), dict)

    @unittest.skipIf(models.storage_t == 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""

    @unittest.skipIf(models.storage_t == 'db', "not testing db storage")
    def test_new(self):
        """test that new adds an object to the database"""

    @unittest.skipIf(models.storage_t == 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""
