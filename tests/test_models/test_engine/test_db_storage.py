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


class TestDBStorage(unittest.TestCase):
    def setUp(self):
        """Prepares test fixtures"""
        self.storage = DBStorage()
        self.storage.reload()

        # Add Fixtures data.
        classes = [Amenity, User, State, City, Place, Review]
        data = {'users': [], 'states': [],
                'cities': [], 'places': [],
                'reviews': [], 'amenities': []}
        for Cls in classes:
            cls_name = Cls.__name__
            for i in list(range(3)):
                name = "{}-{}".format(cls_name, i)
                if cls_name == 'State':
                    data['states'].append(Cls(name=name))
                elif cls_name == 'Amenity':
                    data['amenities'].append(Cls(name=name))
                elif cls_name == 'User':
                    user_d = {'email': 'user{}@test.com'.format(i),
                              'password': '1234',
                              'first_name': 'Fisrt{}'.format(i),
                              'last_name': 'Last{}'.format(i)}
                    data['users'].append(Cls(**user_d))
                elif cls_name == 'City':
                    data['cities'].append(Cls(name=name,
                                              state_id=data['states'][i].id))
                elif cls_name == 'Place':
                    place_d = {'city_id': data['cities'][i].id,
                               'user_id': data['users'][i].id,
                               'name': name, 'description': name,
                               'number_rooms': i + 5,
                               'number_bathrooms': i + 5,
                               'max_guest': i + 5,
                               'price_by_night': (i + 5) * 1.5}
                    data['places'].append(Cls(**place_d))
                elif cls_name == 'Review':
                    data['reviews'].append(Cls(user_id=data['users'][i].id,
                                           place_id=data['places'][i].id,
                                           text=name))

                key = "{}s".format(cls_name).lower()
                if cls_name == "City":
                    key = "cities"
                if cls_name == "Amenity":
                    key = "amenities"
                self.storage.new(data[key][i])
        self.storage.save()
        self.data = data

    def tearDown(self):
        """Runs after each test"""
        self.storage.close()

    """Test the FileStorage class"""
    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(self.storage.all()), dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""
        self.assertEqual(len(self.storage.all()), 18)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """test that new adds an object to the database"""
        classes = [Amenity, City, Place, Review, State, User]

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get(self):
        """Test that get returns the correct object, or None"""
        # Get items with correct class and id.
        for items in self.data.values():
            for obj in items:
                db_obj = self.storage.get(obj.__class__,
                                          obj.id)
                self.assertIsNotNone(db_obj)
                self.assertEqual(obj.id, db_obj.id)
                self.assertEqual(obj.__class__.__name__,
                                 db_obj.__class__.__name__)
        # Get items with correct class and incorrect id.
        self.assertIsNone(self.storage.get(obj.__class__, "45786"))

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count(self):
        """Test that count returns the correct number of items"""
        self.assertEqual(self.storage.count(), 18)
        classes = [Amenity, City, Place, Review, State, User]
        for cls in classes:
            self.assertEqual(self.storage.count(cls), 3)
