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
    @classmethod
    def setUpClass(cls):
        """Set up test instance"""
        cls.storage = FileStorage()

    # Create test objects
        cls.user = User(email="test@example.com", password="test")
        cls.state = State(name="California")

        cls.storage.new(cls.user)
        cls.storage.new(cls.state)
        cls.storage.save()

    @classmethod
    def tearDownClass(cls):
        """Clean up test objects"""
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_all_returns_dict(self):
        """Test that all returns the FileStorage.__objects attr"""
        new_dict = self.storage.all()
        self.assertEqual(type(new_dict), dict)
        self.assertIs(new_dict, self.storage._FileStorage__objects)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_new(self):
        """test that new adds an object to the FileStorage.__objects attr"""
        save = FileStorage._FileStorage__objects
        FileStorage._FileStorage__objects = {}
        test_dict = {}
        for key, value in classes.items():
            with self.subTest(key=key, value=value):
                instance = value()
                instance_key = instance.__class__.__name__ + "." + instance.id
                self.storage.new(instance)
                test_dict[instance_key] = instance
                self.assertEqual(test_dict, self.storage._FileStorage__objects)
        FileStorage._FileStorage__objects = save

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""
        new_dict = {}
        for key, value in classes.items():
            instance = value()
            instance_key = instance.__class__.__name__ + "." + instance.id
            new_dict[instance_key] = instance
        save = FileStorage._FileStorage__objects
        FileStorage._FileStorage__objects = new_dict
        self.storage.save()
        FileStorage._FileStorage__objects = save
        for key, value in new_dict.items():
            new_dict[key] = value.to_dict()
        string = json.dumps(new_dict)
        with open("file.json", "r") as f:
            js = f.read()
        self.assertEqual(json.loads(string), json.loads(js))

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_get_existing_object(self):
        """Test get method retrieves an existing object"""
        user = self.storage.get(User, self.user.id)
        self.assertIsNotNone(user)
        self.assertEqual(user.id, self.user.id)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_get_nonexistent_object(self):
        """Test get method using non-existent object"""
        self.assertIsNone(self.storage.get(User, "nonexistent_id"))

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_get_invalid_class(self):
        """Test get method returns None for an invalid class"""
        self.assertIsNone(self.storage.get("InvalidClass", "1234"))

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_count_all(self):
        """Test count method returns the total number of objects"""
        initial_count = self.storage.count()
        self.assertGreaterEqual(initial_count, 2)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_count_specific_class(self):
        """Test count method returns correct count for a given class"""
        user_count = self.storage.count(User)
        state_count = self.storage.count(State)
        self.assertGreaterEqual(user_count, 1)
        self.assertGreaterEqual(state_count, 1)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_count_invalid_class(self):
        """Test count method returns 0 for an invalid class"""
        self.assertEqual(self.storage.count("InvalidClass"), 0)


if __name__ == "__main__":
    unittest.main()
