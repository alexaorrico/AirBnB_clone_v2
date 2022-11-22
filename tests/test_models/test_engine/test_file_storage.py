#!/usr/bin/python3
"""
Contains the TestFileStorageDocs classes
"""

from datetime import datetime
import inspect
import models
from models import storage
from models.engine import file_storage
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
FileStorage = file_storage.FileStorage
classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class TestFileStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of FileStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.fs_f = inspect.getmembers(FileStorage, inspect.isfunction)

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

    def test_file_storage_module_docstring(self):
        """Test for the file_storage.py module docstring"""
        self.assertIsNot(file_storage.__doc__, None,
                         "file_storage.py needs a docstring")
        self.assertTrue(len(file_storage.__doc__) >= 1,
                        "file_storage.py needs a docstring")

    def test_file_storage_class_docstring(self):
        """Test for the FileStorage class docstring"""
        self.assertIsNot(FileStorage.__doc__, None,
                         "FileStorage class needs a docstring")
        self.assertTrue(len(FileStorage.__doc__) >= 1,
                        "FileStorage class needs a docstring")

    def test_fs_func_docstrings(self):
        """Test for the presence of docstrings in FileStorage methods"""
        for func in self.fs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))

    def test_fs_get_method(self):
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

    def test_fs_count_method(self):
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
    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_all_returns_dict(self):
        """Test that all returns the FileStorage.__objects attr"""
        storage = FileStorage()
        new_dict = storage.all()
        self.assertEqual(type(new_dict), dict)
        self.assertIs(new_dict, storage._FileStorage__objects)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_new(self):
        """test that new adds an object to the FileStorage.__objects attr"""
        storage = FileStorage()
        save = FileStorage._FileStorage__objects
        FileStorage._FileStorage__objects = {}
        test_dict = {}
        for key, value in classes.items():
            with self.subTest(key=key, value=value):
                instance = value()
                instance_key = instance.__class__.__name__ + "." + instance.id
                storage.new(instance)
                test_dict[instance_key] = instance
                self.assertEqual(test_dict, storage._FileStorage__objects)
        FileStorage._FileStorage__objects = save

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""
        storage = FileStorage()
        new_dict = {}
        for key, value in classes.items():
            instance = value()
            instance_key = instance.__class__.__name__ + "." + instance.id
            new_dict[instance_key] = instance
        save = FileStorage._FileStorage__objects
        FileStorage._FileStorage__objects = new_dict
        storage.save()
        FileStorage._FileStorage__objects = save
        for key, value in new_dict.items():
            new_dict[key] = value.to_dict()
        string = json.dumps(new_dict)
        with open("file.json", "r") as f:
            js = f.read()
        self.assertEqual(json.loads(string), json.loads(js))
