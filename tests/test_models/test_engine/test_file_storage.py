#!/usr/bin/python3
"""
Contains the TestFileStorageDocs classes
"""

from datetime import datetime
import inspect
import models
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

    def test_get(self):
        """Test get method to retrieve an object"""
        storage = FileStorage()
        state = State()
        state.name = "California"
        storage.new(state)
        storage.save()

        obj = storage.get(State, state.id)
        self.assertEqual(obj, state)

    def test_get_invalid_class(self):
        """Test retrieving an invalid class"""
        storage = FileStorage()
        state = State()

        with self.assertRaises(AttributeError):
            storage.get(None, state.id)

    def test_get_invalid_id(self):
        """Test get invalid object id"""
        storage = FileStorage()
        self.assertIsNone(storage.get(State, "invalid_id"))

    def test_count_all(self):
        """Test count to aggregate all objects"""
        storage = FileStorage()
        count = len(storage.all())
        self.assertEqual(storage.count(), count)

    def test_count_state(self):
        """Test count state objects"""
        storage = FileStorage()
        states = len(storage.all(State))
        self.assertEqual(storage.count(State), states)

    def test_count_user(self):
        """Test count user objects"""
        storage = FileStorage()
        users = len(storage.all(User))
        self.assertEqual(storage.count(User), users)

    def test_count_amenity(self):
        """Test count amenity objects"""
        storage = FileStorage()
        a = len(storage.all(Amenity))
        self.assertEqual(storage.count(Amenity), a)

    def test_count_city(self):
        """Test count city objects"""
        storage = FileStorage()
        c = len(storage.all(City))
        self.assertEqual(storage.count(City), c)

    def test_count_place(self):
        """Test count place objects"""
        storage = FileStorage()
        p = len(storage.all(Place))
        self.assertEqual(storage.count(Place), p)

    def test_count_review(self):
        """Test count review objects"""
        storage = FileStorage()
        r = len(storage.all(Review))
        self.assertEqual(storage.count(Review), r)

    def test_count_invalid_class(self):
        """Test counting invalid class."""
        storage = FileStorage()
        self.assertEqual(storage.count("Invalid"), 0)
