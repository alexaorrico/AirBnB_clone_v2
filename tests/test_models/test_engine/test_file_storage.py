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

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_get(self):
        """Test that the get property returns the requested object"""
        storage = FileStorage()
        self.assertIs(storage.get("User", "xyz"), None)
        self.assertIs(storage.get("xyz", "xyz"), None)
        new_user = User()
        new_user.save()
        self.assertEqual(storage.get("User", new_user.id), new_user)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_count(self):
        """Test that count works as it should"""
        storage = FileStorage()
        length = len(storage.all())
        self.assertEqual(storage.count(), length)
        state_len = len(storage.all("State"))
        self.assertEqual(storage.count("State"), state_len)
        new_state = State()
        new_state.save()
        self.assertEqual(storage.count(), length + 1)
        self.assertEqual(storage.count("State"), state_len + 1)


class TestFileStorageMethods(unittest.TestCase):

    def setUp(self):
        """Set up a FileStorage instance for testing."""
        self.storage = FileStorage()

    def tearDown(self):
        """Clean up after each test."""
        self.storage._FileStorage__objects = {}

    def test_count_all_objects(self):
        """Test counting all objects in storage."""
        # Create some objects for testing
        BaseModel().save()
        BaseModel().save()
        BaseModel().save()

        # Count all objects
        count = self.storage.count()

        # Check that the count matches the number of created objects
        self.assertEqual(count, 3)

    def test_count_objects_of_specific_class(self):
        """Test counting objects of a specific class."""
        # Create some objects for testing
        BaseModel().save()
        BaseModel().save()
        BaseModel().save()

        # Count objects of the BaseModel class
        count = self.storage.count("BaseModel")

        # Check that the count matches the number of created BaseModel objects
        self.assertEqual(count, 3)

    def test_count_no_objects(self):
        """Test counting when there are no objects in storage."""
        # Count all objects when there are none
        count = self.storage.count()

        # Check that the count is zero
        self.assertEqual(count, 0)

    def test_delete_existing_object(self):
        """Test deleting an existing object from storage."""
        # Create an object and save it
        obj = BaseModel()
        obj.save()

        # Delete the object
        self.storage.delete(obj)

        # Check that the object is no longer in storage
        self.assertIsNone(self.storage.get("BaseModel", obj.id))

    def test_delete_nonexistent_object(self):
        """Test deleting a nonexistent object from storage."""
        # Create an object without saving it
        obj = BaseModel()

        # Try to delete the object
        self.storage.delete(obj)

        # Check that no error occurs
        # Since the object was never saved, it shouldn't be in storage anyway
        self.assertIsNone(self.storage.get("BaseModel", obj.id))



if __name__ == '__main__':
    unittest.main()
