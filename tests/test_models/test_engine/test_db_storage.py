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
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import pep8
import unittest
from uuid import uuid4
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

    def test_db_get_method(self):
        """Test for get method functionalities
           Applicable to both file and db storage
        """
        user = User(first_name="ALX", last_name="Developer",
                    email="dev@alx.com", password="alx_dev_pwd")
        user.save()
        state = State(name="Kenya")
        state.save()
        city = City(name="Nairobi", state_id=state.id)
        city.save()
        place = Place(name="Town House", city_id=city.id, user_id=user.id,
                      number_rooms=4, number_bathrooms=3, max_guest=5,
                      price_by_night=50)
        place.save()

        # check for valid search results
        if os.getenv('HBNB_TYPE_STORAGE') == 'db':
            self.assertTrue(storage.get(User, user.id) is user)
            self.assertTrue(storage.get(State, state.id) is state)
            self.assertTrue(storage.get(City, city.id) is city)
            self.assertTrue(storage.get(Place, place.id) is place)
        else:
            self.assertEqual(storage.get(User, user.id).id, user.id)
            self.assertEqual(storage.get(State, state.id).id,  state.id)
            self.assertEqual(storage.get(City, city.id).id, city.id)
            self.assertEqual(storage.get(Place, place.id).id, place.id)

        # check for empty search results
        self.assertTrue(storage.get(User, str(uuid4())) is None)
        self.assertTrue(storage.get(State, str(uuid4())) is None)
        self.assertTrue(storage.get(City, str(uuid4())) is None)

    def test_db_count_method(self):
        """Test for count method functionalities
           Applicable to both file and db storage
        """
        user = User(first_name="New", last_name="User", email="new@hbnb.com",
                    password="hbnb_user_pwd")
        user.save()
        state = State(name="South Africa")
        state.save()
        city = City(name="Cape Town", state_id=state.id)
        city.save()
        place = Place(name="Outdoor Cottage", city_id=city.id, user_id=user.id,
                      number_rooms=2, number_bathrooms=2, max_guest=3,
                      price_by_night=35)

        place.save()

        # check count of ites
        self.assertTrue(storage.count(User) >= 1)
        self.assertTrue(storage.count(State) >= 1)
        self.assertTrue(storage.count(City) >= 1)
        self.assertTrue(storage.count(Place) >= 1)


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""
    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionary"""
        self.assertIs(type(models.storage.all()), dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """test that new adds an object to the database"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""
