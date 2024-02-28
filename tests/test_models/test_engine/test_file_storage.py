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
FileStorage = file_storage.FileStorage
classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class TestCodeFormat(unittest.TestCase):
    def test_pycodestyle_conformance_file_storage(self):
        """Test that models/engine/file_storage.py conforms to pycodestyle."""
        pycodestyles = pycodestyle.StyleGuide(quiet=True)
        result = pycodestyles.check_files(['models/engine/file_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pycodestyle_conformance_test_file_storage(self):
        """Test tests/test_models/test_engine/test_file_storage.py
        conforms to pycodestyle."""
        pycodestyles = pycodestyle.StyleGuide(quiet=True)
        result = pycodestyles.check_files(
            ['tests/test_models/test_engine/test_file_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")


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


class TestDBStorageMethodsGet(unittest.TestCase):
    """
    Class for Test File Storage Methods Get and count
    """
    @classmethod
    def setUpClass(cls):
        """
        setup tests for class
        """
        print('...... Testing Get() Method ......')

    def setUp(self):
        """
        Set up
        """
        self.storage = FileStorage()
        self.state_obj = State(id=1812)
        self.storage.new(self.state_obj)
        self.storage.save()

    def tearDown(self):
        """
        Clean up after each test
        """
    @unittest.skipIf(models.storage_t != 'db', "not testing file storage")
    def test_get_1(self):
        """Get function"""
        self.assertEqual(self.storage.get(State, 1812), self.state_obj)

    @unittest.skipIf(models.storage_t != 'db', "not testing file storage")
    def test_get_nonexistent(self):
        """Get function"""
        self.assertEqual(self.storage.get(State, 153), None)

    @unittest.skipIf(models.storage_t != 'db', "not testing file storage")
    def test_get_2(self):
        """Get function"""
        self.assertEqual(self.storage.get(State, 153), None)

    @unittest.skipIf(models.storage_t != 'db', "not testing file storage")
    def test_get_invalid_cls(self):
        """Get function"""
        self.assertEqual(self.storage.get(None, 153), None)


class TestStorageCount(unittest.TestCase):
    """Count function"""
    @classmethod
    def setUpClass(cls):
        """
        setup tests for class
        """
        print('...... Testing Count() Method ......')

    def setup(self):
        """
        setup method
        """
        self.storage = FileStorage()
        self.state1 = State(name="California")
        self.state1.save()
        self.state2 = State(name="Colorado")
        self.state2.save()
        self.state3 = State(name="Wyoming")
        self.state3.save()
        self.state4 = State(name="Virgina")
        self.state4.save()
        self.state5 = State(name="Oregon")
        self.state5.save()
        self.state6 = State(name="New_York")
        self.state6.save()
        self.state7 = State(name="Ohio")
        self.state7.save()

    @unittest.skipIf(models.storage_t != 'db', "not testing file storage")
    def test_count_all(self):
        """test  count all states"""
        expected_count = len(self.storage.all())
        self.assertEqual(self.storage.count(), expected_count)

    @unittest.skipIf(models.storage_t != 'db', "not testing file storage")
    def test_count_cls(self):
        """
        test count with specific  class
        """
        expected_count = len(self.storage.all(State))
        self.assertEqual(self.storage.count(State), expected_count)

    @unittest.skipIf(models.storage_t != 'db', "not testing file storage")
    def test_count_all_empty(self):
        """
        Test count with no class specified and storage is empty
        """
        self.storage.all().clear()
        self.assertEqual(self.storage.count(), 0)

    @unittest.skipIf(models.storage_t != 'db', "not testing file storage")
    def test_count_cls_empty(self):
        """
        Test count with a specific class and storage is empty
        """
        self.storage.all().clear()
        self.assertEqual(self.storage.count(State), 0)

class TestFileStorageGetCount(unittest.TestCase):
    def setUp(self):
        self.storage = FileStorage()
        self.place = Place()
        self.review = Review()
        self.user = User()

    @unittest.skipIf(models.storage_t != 'db', "not testing file storage")
    def test_get_with_file_storage(self):
        result = self.storage.get(Place, "some_id")
        expected_msg = "OK"
        self.assertEqual(result, expected_msg, msg=f"Got {result}, expected {expected_msg}")

    @unittest.skipIf(models.storage_t != 'db', "not testing file storage")
    def test_count_with_file_storage(self):
        result = self.storage.count(Place)
        expected_msg = "OK"
        self.assertEqual(result, expected_msg, msg=f"Got {result}, expected {expected_msg}")


if __name__ == '__main__':
    unittest.main()
