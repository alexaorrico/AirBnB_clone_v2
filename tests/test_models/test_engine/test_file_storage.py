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
classes = {
    "Amenity": Amenity,
    "BaseModel": BaseModel,
    "City": City,
    "Place": Place,
    "Review": Review,
    "State": State,
    "User": User,
}


class TestFileStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of FileStorage class"""

    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.fs_f = inspect.getmembers(FileStorage, inspect.isfunction)

    def test_pep8_conformance_file_storage(self):
        """Test that models/engine/file_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(["models/engine/file_storage.py"])
        self.assertEqual(
            result.total_errors, 0, "Found code style errors (and warnings)."
        )

    def test_pep8_conformance_test_file_storage(self):
        """Test tests/test_models/test_file_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(
            [
                "tests/test_models/test_engine/\
test_file_storage.py"
            ]
        )
        self.assertEqual(
            result.total_errors, 0, "Found code style errors (and warnings)."
        )

    def test_file_storage_module_docstring(self):
        """Test for the file_storage.py module docstring"""
        self.assertIsNot(
            file_storage.__doc__, None, "file_storage.py needs a docstring"
        )
        self.assertTrue(
            len(file_storage.__doc__) >= 1, "file_storage.py needs a docstring"
        )

    def test_file_storage_class_docstring(self):
        """Test for the FileStorage class docstring"""
        self.assertIsNot(
            FileStorage.__doc__, None, "FileStorage class needs a docstring"
        )
        self.assertTrue(
            len(FileStorage.__doc__) >= 1, "FileStorage class needs a docstring"
        )

    def test_fs_func_docstrings(self):
        """Test for the presence of docstrings in FileStorage methods"""
        for func in self.fs_f:
            self.assertIsNot(
                func[1].__doc__, None, "{:s} method needs a docstring".format(func[0])
            )
            self.assertTrue(
                len(func[1].__doc__) >= 1,
                "{:s} method needs a docstring".format(func[0]),
            )


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""

    @unittest.skipIf(models.storage_t == "db", "not testing file storage")
    def test_all_returns_dict(self):
        """Test that all returns the FileStorage.__objects attr"""
        storage = FileStorage()
        new_dict = storage.all()
        self.assertEqual(type(new_dict), dict)
        self.assertIs(new_dict, storage._FileStorage__objects)

    @unittest.skipIf(models.storage_t == "db", "not testing file storage")
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

    @unittest.skipIf(models.storage_t == "db", "not testing file storage")
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

    @unittest.skipIf(models.storage_t == "db", "not testing file storage")
    def test_get(self):
        """test that get returns an object based on class and id"""
        storage = FileStorage()
        new_dict = {}
        for key, value in classes.items():
            instance = value()
            instance_key = instance.__class__.__name__ + "." + instance.id
            new_dict[instance_key] = instance
        save = FileStorage._FileStorage__objects
        FileStorage._FileStorage__objects = new_dict
        for key, value in classes.items():
            instance = storage.get(value, instance.id)
            self.assertIs(instance, new_dict[value.__name__ + "." + instance.id])
        FileStorage._FileStorage__objects = save

    @unittest.skipIf(models.storage_t == "db", "not testing file storage")
    def test_count(self):
        """test that count returns the number of objects in storage"""
        storage = FileStorage()
        new_dict = {}
        for key, value in classes.items():
            instance = value()
            instance_key = instance.__class__.__name__ + "." + instance.id
            new_dict[instance_key] = instance
        save = FileStorage._FileStorage__objects
        FileStorage._FileStorage__objects = new_dict
        self.assertEqual(storage.count(), len(new_dict))
        FileStorage._FileStorage__objects = save

    @unittest.skipIf(models.storage_t == "db", "not testing file storage")
    def test_count_class(self):
        """test that count returns the number of objects in storage matching the class"""
        storage = FileStorage()
        new_dict = {}
        for key, value in classes.items():
            instance = value()
            instance_key = instance.__class__.__name__ + "." + instance.id
            new_dict[instance_key] = instance
        save = FileStorage._FileStorage__objects
        FileStorage._FileStorage__objects = new_dict
        for key, value in classes.items():
            self.assertEqual(storage.count(value), 1)
        FileStorage._FileStorage__objects = save

    @unittest.skipIf(models.storage_t == "db", "not testing file storage")
    def test_count_none(self):
        """test that count returns 0 when no class is passed"""
        storage = FileStorage()
        self.assertEqual(storage.count(), 0)

    @unittest.skipIf(models.storage_t == "db", "not testing file storage")
    def test_count_class_none(self):
        """test that count returns 0 when no class is passed"""
        storage = FileStorage()
        self.assertEqual(storage.count(None), 0)

    @unittest.skipIf(models.storage_t == "db", "not testing file storage")
    def test_get_none(self):
        """test that get returns None when no class or id matches"""
        storage = FileStorage()
        self.assertIs(storage.get(None, None), None)
        self.assertIs(storage.get(None, "1234"), None)
        self.assertIs(storage.get(State, None), None)
        self.assertIs(storage.get("State", "1234"), None)

    @unittest.skipIf(models.storage_t == "db", "not testing file storage")
    def test_new_no_class(self):
        """Test that new adds an object to the database"""
        storage = FileStorage()
        new_state = State(name="California")
        storage.new(new_state)
        storage.save()
        self.assertIsNot(storage.get(State, new_state.id), None)

    @unittest.skipIf(models.storage_t == "db", "not testing file storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""
        storage = FileStorage()
        new_state = State(name="California")
        storage.new(new_state)
        storage.save()
        self.assertEqual(len(storage.all()), 1)
        new_state = State(name="Nevada")
        storage.new(new_state)
        storage.save()
        self.assertEqual(len(storage.all()), 2)

    @unittest.skipIf(models.storage_t == "db", "not testing file storage")
    def test_delete(self):
        """Test that delete removes an object from __objects if it exists"""
        storage = FileStorage()
        new_state = State(name="California")
        storage.new(new_state)
        storage.save()
        self.assertIsNot(storage.get(State, new_state.id), None)
        storage.delete(new_state)
        storage.save()
        self.assertIs(storage.get(State, new_state.id), None)

    @unittest.skipIf(models.storage_t == "db", "not testing file storage")
    def test_delete_none(self):
        """Test that delete does nothing if the object does not exist"""
        storage = FileStorage()
        new_state = State(name="California")
        storage.new(new_state)
        storage.save()
        self.assertIsNot(storage.get(State, new_state.id), None)
        storage.delete(State(name="Nevada"))
        storage.save()
        self.assertIsNot(storage.get(State, new_state.id), None)
