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
import pycodestyle
import unittest
from models import storage
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage

FileStorage = file_storage.FileStorage
classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class TestFileStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of FileStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.fs_f = inspect.getmembers(FileStorage, inspect.isfunction)

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
    def test_count(self):
        """Test the count method."""
        # Initial count
        initial_count = storage.count(State)

        # Create a new object and save it
        obj = State()
        # Assuming there's a save method to persist changes
        storage.new(obj)
        storage.save()

        # Verify the count has increased by 1
        new_count = storage.count(State)
        self.assertEqual(initial_count + 1, new_count,
                         "Count should increase by 1 after adding an object.")

        # Clean up by deleting the created object
        storage.delete(obj)
        storage.save()

        # Verify the count has returned to the initial value
        final_count = storage.count(State)
        self.assertEqual(initial_count, final_count,
                         "Count should return to initial value after deletion")

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_get(self):
        """Test creating an object, retrieving it, and then deleting it."""
        # Setup: Create a new object and save it
        created_model = State()
        created_model.save()

        # Attempt to retrieve the object using the get method
        retrieved_model = storage.get(State, created_model.id)

        # Assertions to ensure the retrieved object matches the created object
        self.assertIsNotNone(retrieved_model, "Failed to retrieve the model.")
        self.assertEqual(created_model.id, retrieved_model.id,
                         "Retrieved model ID does not match the created model")

        # Teardown: Delete the created object to clean up
        # Assuming your storage has a delete method. This part may vary.
        storage.delete(created_model)
        storage.save()

        # Verify deletion
        deleted_model = storage.get(State, created_model.id)
        self.assertIsNone(deleted_model, "Model was not deleted successfully.")
