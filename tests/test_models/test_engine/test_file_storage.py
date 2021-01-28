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
    """
    def test_pep8_conformance_test_file_storage(self):
        Test tests/test_models/test_file_storage.py conforms to PEP8.
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_file_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")"""

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
    @unittest.skipIf(os.getenv(
        'HBNB_TYPE_STORAGE') == "db", "not testing file storage")
    def test_all_returns_dict(self):
        """Test that all returns the FileStorage.__objects attr"""
        storage = FileStorage()
        new_dict = storage.all()
        self.assertEqual(type(new_dict), dict)
        self.assertIs(new_dict, storage._FileStorage__objects)

    @unittest.skipIf(os.getenv(
        'HBNB_TYPE_STORAGE') == "db", "not testing file storage")
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

    @unittest.skipIf(os.getenv(
        'HBNB_TYPE_STORAGE') == "db", "not testing file storage")
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

    def test_get_file_st(self):
        """testing get method with State class"""
        d1 = {"name": "Test0"}
        new_state1 = State(**d1)
        storage.new(new_state1)
        storage.save()
        st1 = storage.get(State, new_state1.id)
        self.assertEqual(new_state1, st1)

    def test_get_file_ct(self):
        """testing get method with City class"""
        d1 = {"name": "Test0"}
        new_city1 = City(**d1)
        storage.new(new_city1)
        storage.save()
        ct1 = storage.get(City, new_city1.id)
        self.assertEqual(new_city1, ct1)

    def test_get_file_us(self):
        """testing get method with User class"""
        d1 = {"email": "email", "password": "password"}
        new_user1 = User(**d1)
        storage.new(new_user1)
        storage.save()
        us1 = storage.get(User, new_user1.id)
        self.assertEqual(new_user1, us1)

    def test_get_file_am(self):
        """testing get method with Amenity class"""
        d1 = {"name": "name"}
        new_amenity1 = Amenity(**d1)
        storage.new(new_amenity1)
        storage.save()
        am1 = storage.get(Amenity, new_amenity1.id)
        self.assertEqual(new_amenity1, am1)

    def test_get_file_pl(self):
        """testing get method with Place class"""
        new_us = User(name="user")
        d1 = {"name": "place", "user_id": new_us.id}
        new_place1 = Place(**d1)
        storage.new(new_place1)
        storage.save()
        pl1 = storage.get(Place, new_place1.id)
        self.assertEqual(new_place1, pl1)

    def test_get_file_rv(self):
        """testing get method with Review class"""
        new_us = User(name="user1")
        d1 = {"text": "testing", "user_id": new_us.id}
        new_review1 = Review(**d1)
        storage.new(new_review1)
        storage.save()
        rv1 = storage.get(Review, new_review1.id)
        self.assertEqual(new_review1, rv1)

    def test_get_file_id(self):
        """testing get method with a wrong id"""
        get_state = storage.get(State, "2456jffghj")
        self.assertEqual(get_state, None)

    def test_count_file(self):
        """Testing count method"""
        len_1 = len(storage.all())
        count_1 = storage.count()
        self.assertEqual(len_1, count_1)

    def test_count_db_state(self):
        """Testing count method for a State class"""
        len_state = len(storage.all(State))
        count_state = storage.count(State)
        self.assertEqual(len_state, count_state)
