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
        """Test tests/test_models/test_engine/test_file_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/test_file_storage.py'])
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
    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db', "not testing file storage")
    def test_all(self):
        """Test that all returns the dictionary __objects"""
        storage = FileStorage()
        all_objs = storage.all()
        self.assertIsNot(all_objs, None, "all() must return a dict")
        self.assertEqual(type(all_objs), dict, "all() must return a dict")

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db', "not testing file storage")
    def test_new(self):
        """Test that new adds an object to the __objects"""
        storage = FileStorage()
        new_state = State(name="New York")
        new_state.save()
        all_objs = storage.all(State)
        self.assertTrue(all_objs[new_state.id] == new_state, "State not added to __objects")

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db', "not testing file storage")
    def test_save(self):
        """Test that save properly saves objects to the JSON file"""
        storage = FileStorage()
        new_state = State(name="Texas")
        new_state.save()
        storage.save()
        with open("file.json", "r") as f:
            data = json.load(f)
            key = "State." + new_state.id
            self.assertIsNot(data.get(key), None, "State not saved to JSON file")

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db', "not testing file storage")
    def test_get(self):
        """Test that get retrieves an object by class and ID"""
        storage = FileStorage()
        new_state = State(name="California")
        new_state.save()
        retrieved_state = storage.get(State, new_state.id)
        self.assertEqual(retrieved_state, new_state, "State not retrieved correctly")

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db', "not testing file storage")
    def test_count(self):
        """Test that count returns the correct count of objects in storage"""
        storage = FileStorage()
        state_count = storage.count(State)
        new_state = State(name="Texas")
        new_state.save()
        updated_state_count = storage.count(State)
        self.assertEqual(updated_state_count, state_count + 1, "Count not updated correctly")

if __name__ == "__main__":
    unittest.main()
