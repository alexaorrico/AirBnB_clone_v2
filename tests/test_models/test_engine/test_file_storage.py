#!/usr/bin/python3
"""
Contains the TestFileStorageDocs and TestFileStorage classes
"""

from datetime import datetime
import inspect
import json
import os
import pep8
import unittest
from models.engine.file_storage import FileStorage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

FileStorage = FileStorage
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

    def test_file_storage_module_docstring(self):
        """Test for the file_storage.py module docstring"""
        self.assertIsNot(FileStorage.__doc__, None,
                         "file_storage.py needs a docstring")
        self.assertTrue(len(FileStorage.__doc__) >= 1,
                        "file_storage.py needs a docstring")

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
    def setUp(self):
        """Set up the tests"""
        self.storage = FileStorage()
        self.storage.reload()
        self.new_user = User(email="test@example.com", password="testpass")

    def tearDown(self):
        """Clean up after each test"""
        if os.path.exists("file.json"):
            os.remove("file.json")

    def test_all_returns_dict(self):
        """Test that all returns the FileStorage.__objects attr"""
        all_objs = self.storage.all()
        self.assertIsInstance(all_objs, dict)
        self.assertIs(all_objs, self.storage._FileStorage__objects)

    def test_new(self):
        """Test that new adds an object to the FileStorage.__objects attr"""
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

    def test_all_with_class(self):
        """Test that all with class parameter returns correct objects"""
        self.storage.new(self.new_user)
        self.storage.save()
        key = 'User.' + self.new_user.id
        all_objs = self.storage.all(User)
        self.assertIn(key, all_objs)
        self.assertEqual(all_objs[key], self.new_user)

    def test_all_with_invalid_class(self):
        """Test that all with invalid class parameter returns an empty dict"""
        all_objs = self.storage.all("InvalidClass")
        self.assertEqual(all_objs, {})

    def test_reload_with_invalid_data(self):
        """Test that reload with invalid data does not raise an error"""
        invalid_data = "Invalid JSON data"
        self.storage._FileStorage__objects = invalid_data
        self.storage.reload()

    def test_delete_with_invalid_object(self):
        """Test that delete with invalid object does nothing"""
        invalid_obj = "InvalidObject"
        self.storage.delete(invalid_obj)

    def test_delete_with_valid_object(self):
        """Test that delete removes the object from __objects"""
        self.storage.new(self.new_user)
        self.storage.save()
        key = 'User.' + self.new_user.id
        self.assertIn(key, self.storage.all())
        self.storage.delete(self.new_user)
        self.assertNotIn(key, self.storage.all())

    def test_close_with_open_session(self):
        """Test that close with an open session does not raise an error"""
        self.storage.close()

    def test_all_after_delete(self):
        """Test that all returns correct objects after deleting an object"""
        self.storage.new(self.new_user)
        self.storage.save()
        key = 'User.' + self.new_user.id
        self.assertIn(key, self.storage.all())
        self.storage.delete(self.new_user)
        self.assertNotIn(key, self.storage.all())

    def test_all_after_reload(self):
        """Test that all returns correct objects after reloading the storage"""
        self.storage.new(self.new_user)
        self.storage.save()
        key = 'User.' + self.new_user.id
        self.storage.reload()
        self.assertIn(key, self.storage.all())

    def test_new_with_invalid_object(self):
        """Test that new with an invalid object does nothing"""
        invalid_obj = "InvalidObject"
        self.storage.new(invalid_obj)

    def test_save_with_invalid_data(self):
        """Test that save with invalid data does not raise an error"""
        invalid_data = "Invalid JSON data"
        self.storage._FileStorage__objects = invalid_data
        self.storage.save()

    def test_all_returns_empty_dict_after_delete(self):
        """Test that all returns an empty dict after deleting all objects"""
        self.storage.new(self.new_user)
        self.storage.save()
        key = 'User.' + self.new_user.id
        self.assertIn(key, self.storage.all())
        self.storage.delete(self.new_user)
        self.assertNotIn(key, self.storage.all())
        self.assertEqual(self.storage.all(), {})

    def test_save_after_delete(self):
        """Test that save works correctly after deleting an object"""
        self.storage.new(self.new_user)
        self.storage.save()
        key = 'User.' + self.new_user.id
        self.assertIn(key, self.storage.all())
        self.storage.delete(self.new_user)
        self.assertNotIn(key, self.storage.all())
        self.storage.save()

    def test_close_after_delete(self):
        """Test that close works correctly after deleting an object"""
        self.storage.new(self.new_user)
        self.storage.save()
        key = 'User.' + self.new_user.id
        self.assertIn(key, self.storage.all())
        self.storage.delete(self.new_user)
        self.assertNotIn(key, self.storage.all())
        self.storage.close()

    def test_all_after_close(self):
        """Test that all returns correct objects after closing the storage"""
        self.storage.new(self.new_user)
        self.storage.save()
        key = 'User.' + self.new_user.id
        self.storage.close()
        self.storage = FileStorage()
        all_objs = self.storage.all()
        self.assertIn(key, all_objs)
        self.assertEqual(all_objs[key], self.new_user)

    def test_new_after_close(self):
        """Test that new works correctly after closing the storage"""
        self.storage.new(self.new_user)
        self.storage.save()
        key = 'User.' + self.new_user.id
        self.storage.close()
        self.storage = FileStorage()
        new_user_2 = User(email="new_test@example.com", password="new_testpass")
        self.storage.new(new_user_2)
        self.assertIn(key, self.storage.all())
        self.assertEqual(self.storage.all()[key], new_user_2)

if __name__ == "__main__":
    unittest.main()
