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

    def test_get_method_docstring(self):
        """Test for the get method docstring"""
        self.assertIsNot(DBStorage.get.__doc__, None,
                         "get method needs a docstring")
        self.assertTrue(len(DBStorage.get.__doc__) >= 1,
                        "get method needs a docstring")

    def test_count_method_docstring(self):
        """Test for the count method docstring"""
        self.assertIsNot(DBStorage.count.__doc__, None,
                         "count method needs a docstring")
        self.assertTrue(len(DBStorage.count.__doc__) >= 1,
                        "count method needs a docstring")

    def test_get_method_returns_none(self):
        """Test if get method returns None for non-existent object"""
        # Assuming there is no object with ID 'nonexistent_id' in any class
        result = self.storage.get(SomeClass, 'nonexistent_id')
        self.assertIsNone(result, "get method should return None for non-existent object")

    def test_get_method_returns_object(self):
        """Test if get method returns the correct object"""
        # Assuming there is an object with ID 'existing_id' in SomeClass
        obj = SomeClass()  # Replace with actual class instantiation and ID
        self.storage.__session.add(obj)
        self.storage.__session.commit()
        result = self.storage.get(SomeClass, 'existing_id')
        self.assertEqual(result, obj, "get method should return the correct object")

    def test_count_method_all_objects(self):
        """Test if count method returns the count of all objects"""
        # Assuming there are some objects in the storage
        total_objects = self.storage.count()
        self.assertGreaterEqual(total_objects, 0, "count method should return count of all objects")

    def test_count_method_specific_class(self):
        """Test if count method returns the count of objects for a specific class"""
        # Assuming there are some objects of SomeClass in the storage
        class_objects = self.storage.count(SomeClass)
        self.assertGreaterEqual(class_objects, 0, "count method should return count of specific class objects")

    def test_count_method_no_objects(self):
        """Test if count method returns 0 for no objects"""
        # Assuming there are no objects in the storage
        total_objects = self.storage.count()
        self.assertEqual(total_objects, 0, "count method should return 0 for no objects")


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

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get_existing_object(self):
        """Test retrieving an existing object by ID"""
        new_user = User(email="test@example.com", password="testpassword")
        models.storage.new(new_user)
        models.storage.save()
        retrieved_user = models.storage.get(User, new_user.id)
        self.assertEqual(retrieved_user, new_user)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get_nonexistent_object(self):
        """Test retrieving a nonexistent object by ID"""
        retrieved_user = models.storage.get(User, "nonexistent_id")
        self.assertIsNone(retrieved_user)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count_all_objects(self):
        """Test counting all objects in storage"""
        count_all = models.storage.count()
        total_objects = sum(models.storage.count(cls) for cls in classes.values())
        self.assertEqual(count_all, total_objects)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count_specific_class_objects(self):
        """Test counting objects of a specific class in storage"""
        new_state = State(name="California")
        models.storage.new(new_state)
        models.storage.save()
        count_states = models.storage.count(State)
        self.assertEqual(count_states, 1)
