#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
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
classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.fs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_file_storage(self):
        """Test that models/engine/file_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/file_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_file_storage(self):
        """Test tests/test_models/test_file_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_file_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_file_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "State class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "State class needs a docstring")

    def test_fs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.fs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestDBStorage(unittest.TestCase):
    """Test the DBStorage class"""

    @classmethod
    def setUpClass(cls):
        """Set up class"""
        self.create_data()

    def create_data():
        """Creating Test Data"""
        ca_state = State(name='California')

        pa_city = City(name='Palo Alto', state_id=ca_state.id)
        sf_city = City(name='San Francisco', state_id=ca_state.id)

        am_user = User(first_name='Julian', last_name='Cano',
                       email='1591@holbertonschool.com',
                       password='J00ee12')
        ab_user = User(first_name='Juan', last_name='Gomez',
                       email='1592@holbertonschool.com',
                       password='Yrer')

        home_amenity = Amenity(name="Wifi")
        sav_amenity = Amenity(name="Washer")

        home_place = Place(name='Tall Tree House',
                           city_id=pa_city.id,
                           amenity_id=home_amenity.id,
                           user_id=am_user.id)
        sav_place = Place(name='San Antonio Villa',
                          city_id=pa_city.id,
                          amenity_id=sav_amenity.id,
                          user_id=ab_user.id)

        home_review = Review(text="Is a dope house",
                             place_id=home_place.id,
                             user_id=ab_user.id)
        sav_review = Review(text="Is a wack villa",
                            place_id=home_place.id,
                            user_id=am_user.id)

    def test_all_returns_dict(self):
        """Test that all returns the DBStorage.__objects attr"""
        storage = DBStorage()
        new_dict = storage.all()
        self.assertEqual(type(new_dict), dict)
        self.assertIs(new_dict, storage._DBStorage__objects)

    def test_new(self):
        """test that new adds an object to the DBStorage.__objects attr"""
        storage = DBStorage()
        save = DBStorage._DBStorage__objects
        DBStorage._DBStorage__objects = {}
        test_dict = {}
        for key, value in classes.items():
            with self.subTest(key=key, value=value):
                instance = value()
                instance_key = instance.__class__.__name__ + "." + instance.id
                storage.new(instance)
                test_dict[instance_key] = instance
                self.assertEqual(test_dict, storage._DBStorage__objects)
        DBStorage._DBStorage__objects = save

    def test_save(self):
        """Test that save properly saves objects to file.json"""
        os.remove("file.json")
        storage = DBStorage()
        new_dict = {}
        for key, value in classes.items():
            instance = value()
            instance_key = instance.__class__.__name__ + "." + instance.id
            new_dict[instance_key] = instance
        save = DBStorage._DBStorage__objects
        DBStorage._DBStorage__objects = new_dict
        storage.save()
        DBStorage._DBStorage__objects = save
        for key, value in new_dict.items():
            new_dict[key] = value.to_dict()
        string = json.dumps(new_dict)
        with open("file.json", "r") as f:
            js = f.read()
        self.assertEqual(json.loads(string), json.loads(js))
