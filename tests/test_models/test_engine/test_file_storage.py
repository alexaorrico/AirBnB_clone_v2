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
     def test_state(self):
        """test State creation with a keyword argument"""
        a = State(name="Kamchatka", id="Kamchatka666")
        a.save()
        self.assertIn("Kamchatka666", storage.all("State").keys())

    def test_count(self):
        """test count all"""
        test_len = len(storage.all())
        a = Amenity(name="test_amenity")
        a.save()
        self.assertEqual(test_len + 1, storage.count())
        b = State(name="State test count")
        b.save()
        self.assertEqual(test_len + 2, storage.count())
        storage.delete(b)
        self.assertEqual(test_len + 1, storage.count())

    def test_count_amenity(self):
        """test count with an argument"""
        test_len = len(storage.all("Amenity"))
        a = Amenity(name="test_amenity_2")
        a.save()
        self.assertEqual(test_len + 1, storage.count("Amenity"))
        storage.delete(a)
        self.assertEqual(test_len, storage.count("Amenity"))

    def test_count_state(self):
        """test count with an argument"""
        test_len = len(storage.all("State"))
        a = State(name="test_state_count_arg")
        a.save()
        self.assertEqual(test_len + 1, storage.count("State"))
        storage.delete(a)
        self.assertEqual(test_len, storage.count("State"))

    def test_count_bad_arg(self):
        """test count with dummy class name"""
        self.assertEqual(-1, storage.count("Dummy"))

    def test_get_amenity(self):
        """test get with valid cls and id"""
        a = Amenity(name="test_amenity3", id="test_3")
        a.save()
        result = storage.get("Amenity", "test_3")
        self.assertEqual(a.name, result.name)
        # does not work as the database loses last argument tzinfo for datetime
        # self.assertEqual(a.created_at, result.created_at)
        self.assertEqual(a.created_at.year, result.created_at.year)
        self.assertEqual(a.created_at.month, result.created_at.month)
        self.assertEqual(a.created_at.day, result.created_at.day)
        self.assertEqual(a.created_at.hour, result.created_at.hour)
        self.assertEqual(a.created_at.minute, result.created_at.minute)
        self.assertEqual(a.created_at.second, result.created_at.second)
        storage.delete(a)
        result = storage.get("Amenity", "test_3")
        self.assertIsNone(result)

    def test_get_state(self):
        """test get with valid cls and id"""
        a = State(name="test_state3", id="test_3")
        a.save()
        result = storage.get("State", "test_3")
        self.assertEqual(a.name, result.name)
        # does not work as the database loses last argument tzinfo for datetime
        # self.assertEqual(a.created_at, result.created_at)
        self.assertEqual(a.created_at.year, result.created_at.year)
        self.assertEqual(a.created_at.month, result.created_at.month)
        self.assertEqual(a.created_at.day, result.created_at.day)
        self.assertEqual(a.created_at.hour, result.created_at.hour)
        self.assertEqual(a.created_at.minute, result.created_at.minute)
        self.assertEqual(a.created_at.second, result.created_at.second)
        storage.delete(a)
        result = storage.get("State", "test_3")
        self.assertIsNone(result)

    def test_get_bad_cls(self):
        """test get with invalid cls"""
        result = storage.get("Dummy", "test")
        self.assertIsNone(result)

    def test_get_bad_id(self):
        """test get with invalid id"""
        result = storage.get("State", "very_bad_id")
        self.assertIsNone(result)


if __name__ == "__main__":
    import sys
    import os
    sys.path.insert(1, os.path.join(os.path.split(__file__)[0], '../../..'))
    from models import *
    from models.engine.file_storage import FileStorage
    unittest.main()
