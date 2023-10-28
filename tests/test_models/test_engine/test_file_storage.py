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
    def setUp(self):
        """Set up the class"""

        self.new_dict = {}
        self.file_test = 'test.json'
        self.save = FileStorage._FileStorage__objects
        self.save_file = FileStorage._FileStorage__file_path
        self.storage = FileStorage()
        FileStorage._FileStorage__file_path = self.file_test

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def tearDown(self):
        """To remove any files created"""
        FileStorage._FileStorage__objects = self.save
        FileStorage._FileStorage__filename = self.save_file
        self.new_dict = {}
        try:
            os.remove(self.file_test)
        except FileNotFoundError:
            pass

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_all_returns_dict(self):
        """Test that all returns the FileStorage.__objects attr"""
        self.new_dict = self.storage.all()
        self.assertEqual(type(self.new_dict), dict)
        self.assertIs(self.new_dict, self.storage._FileStorage__objects)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_new(self):
        """test that new adds an object to the FileStorage.__objects attr"""
        FileStorage._FileStorage__objects = {}
        test_dict = {}
        for key, value in classes.items():
            with self.subTest(key=key, value=value):
                instance = value()
                instance_key = instance.__class__.__name__ + "." + instance.id
                self.storage.new(instance)
                test_dict[instance_key] = instance
                self.assertEqual(test_dict, self.storage._FileStorage__objects)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""
        for key, value in classes.items():
            instance = value()
            instance_key = instance.__class__.__name__ + "." + instance.id
            self.new_dict[instance_key] = instance
        FileStorage._FileStorage__objects = self.new_dict
        self.storage.save()
        for key, value in self.new_dict.items():
            self.new_dict[key] = value.to_dict()
        string = json.dumps(self.new_dict)
        with open(self.file_test, "r") as f:
            js = f.read()
        self.assertEqual(json.loads(string), json.loads(js))

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_get(self):
        """Test get to ensure it gets the right objects"""
        for key, value in classes.items():
            instance = value()
            instance_key = type(instance).__name__ + "." + instance.id
            self.new_dict[instance_key] = instance
        FileStorage._FileStorage__objects = self.new_dict
        self.storage.save()

        for key, value in self.new_dict.items():
            cls_obj = classes[key.split('.')[0]]
            cls_id = key.split('.')[1]
            result = self.storage.get(cls_obj, cls_id)
            with self.subTest(key=key, value=value, id=cls_id, cls=cls_obj):
                self.assertIsNotNone(result)

        # Test for when its None
        data = list(classes.values())
        info_for_none = self.storage.get(data[0], data[3])
        self.assertIsNone(info_for_none)

        info_for_none_2 = self.storage.get()
        self.assertIsNone(info_for_none_2)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_count(self):
        """Test count to ensure it count the accurate number of objects"""
        for key, value in classes.items():
            instance = value()
            instance_key = type(instance).__name__ + "." + instance.id
            self.new_dict[instance_key] = instance
        FileStorage._FileStorage__objects = self.new_dict
        self.storage.save()
        data = list(classes.values())
        self.assertEqual(len(self.new_dict), self.storage.count())
        self.assertEqual(1, self.storage.count(data[2]))
