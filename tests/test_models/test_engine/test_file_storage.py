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

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_get_fails(self):
        """"Tests if method retrieves one object"""
        storage = FileStorage()
        self.assertIs(storage.get(User, "Geoff"), None)
        self.assertEqual(storage.get(State, "California"), None)
        self.assertEqual(storage.get(Review, "Fake key"), None)
        self.assertEqual(storage.get(Amenity, "Not amenity"), None)
        self.assertEqual(storage.get(Place, "Not a palce"), None)
        self.assertEqual(storage.get(City, "State"), None)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_get_success(self):
        """ test for successful object retrival """
        storage = FileStorage()
        new_state = State()
        new_city = City()
        new_state.save()
        new_city.save()

        found_city = storage.get(City, new_city.id)
        found_state = storage.get(State, new_state.id)
        wrong_city = storage.get(City, "1234")
        wrong_state = storage.get(State, "12345")
        self.assertEqual(found_state, new_state)
        self.assertIs(found_state, new_state)
        self.assertIsInstance(found_state, State)
        self.assertNotEqual(found_state, None)
        self.assertIsNot(found_state, None)

        self.assertEqual(found_city, new_city)
        self.assertIs(found_city, new_city)
        self.assertIsInstance(found_city, City)
        self.assertNotEqual(found_city, None)
        self.assertIsNot(found_city, None)
        new_state.delete()
        new_city.delete()

    @unittest.skipIf(models.storage_t == 'db', "not testing db storage")
    def test_count(self):
        """""Test if count method counts number of objects in storage"""
        storage = FileStorage()
        count = storage.count()
        count_u = storage.count(User)
        count_s = storage.count(State)
        new_state = State(name='CT')
        new_state.save()
        new_user = User(email="new@fake.com", password="abc")
        new_user.save()
        self.assertEqual(storage.count(), count + 2)
        self.assertNotEqual(storage.count(User), count_u)
        self.assertIsInstance(storage.count(), int)
        self.assertNotEqual(storage.count(State), count_s)
        self.assertIsInstance(storage.count(State), int)
        self.assertNotEqual(storage.count(), None)
        self.assertEqual(storage.count(), storage.count(None))
        new_user.delete()
        new_state.delete()
