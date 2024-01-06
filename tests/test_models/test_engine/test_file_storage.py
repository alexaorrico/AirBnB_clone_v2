#!/usr/bin/python3
"""
Contains the TestFileStorageDocs and TestFileStorage classes
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
        """Test tests/test_models/test_engine/test_file_storage.py conforms"""
        pep8s = pep8.StyleGuide(quiet=True)
        files = ['tests/test_models/test_engine/test_file_storage.py']
        result = pep8s.check_files(files)
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

    @classmethod
    def setUpClass(cls):
        """Set up for the tests"""
        cls.storage = FileStorage()

    @classmethod
    def tearDownClass(cls):
        """Clean up after the tests"""
        del cls.storage

    def test_file_path(self):
        """Test the file_path method"""
        file_path = self.storage._FileStorage__file_path
        self.assertEqual(file_path, "file.json")

    def test_objects(self):
        """Test the objects method"""
        objects = self.storage.all()
        self.assertIs(objects, self.storage._FileStorage__objects)

    def test_all(self):
        """Test the all method"""
        objects = self.storage.all()
        self.assertIsInstance(objects, dict)
        self.assertIs(objects, self.storage._FileStorage__objects)

    def test_new(self):
        """Test the new method"""
        obj = BaseModel()
        self.storage.new(obj)
        obj_key = "{}.{}".format(obj.__class__.__name__, obj.id)
        objects = self.storage.all()
        self.assertIn(obj_key, objects.keys())
        self.assertIs(objects[obj_key], obj)

    def test_save(self):
        """Test the save method"""
        obj = BaseModel()
        self.storage.new(obj)
        self.storage.save()
        file_path = self.storage._FileStorage__file_path
        self.assertTrue(os.path.exists(file_path))
        with open(file_path, 'r') as file:
            content = file.read()
            self.assertIn(obj.__class__.__name__, content)
            self.assertIn(obj.id, content)

    def test_reload(self):
        """Test the reload method"""
        obj = BaseModel()
        self.storage.new(obj)
        self.storage.save()
        self.storage.reload()
        obj_key = "{}.{}".format(obj.__class__.__name__, obj.id)
        objects = self.storage.all()
        self.assertIn(obj_key, objects.keys())
        self.assertIsInstance(objects[obj_key], BaseModel)

    def test_get(self):
        """Test the get method"""
        obj = BaseModel()
        self.storage.new(obj)
        selfstorage.save()

        retrieved_obj = self.storage.get(BaseModel, obj.id)
        self.assertEqual(retrieved_obj, obj)

    def test_count(self):
        """Test the count method"""
        initial_count = self.storage.count()
        obj = BaseModel()
        self.storage.new(obj)
        updated_count = self.storage.count()
        self.assertEqual(updated_count, initial_count + 1)
        obj2 = State()
        self.storage.new(obj2)
        updated_count2 = self.storage.count(State)
        self.assertEqual(updated_count2, 1)


if __name__ == '__main__':
    unittest.main()
