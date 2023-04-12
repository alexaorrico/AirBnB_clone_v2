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
    def __init__(self, methodName: str = "runTest"):
        """
        Wipe out all the previous json file data
        before doing the tests.
        """
        unittest.TestCase.__init__(self, methodName)
        self.storage = FileStorage()
        self.storage._FileStorage__objects = {}
        self.storage.save()

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_all_returns_dict(self):
        """Test that all returns the FileStorage.__objects attr"""
        new_dict = self.storage.all()
        self.assertEqual(type(new_dict), dict)
        self.assertIs(new_dict, self.storage._FileStorage__objects)

        self.assertEqual({}, self.storage.all())
        # If the self.storage.__objects dictionary is still full,
        # even when we haven't added anything to it,
        # we know our tests have already failed to wipe out
        # any test data from the previous time testing here.

    def test_get(self):
        """
        Test that
        'self.storage.get' returns
        an instance of class 'cls' arguments
        with 'id' argument as its 'id' field
        if it was placed in the 'self.storage'
        variale,
        'None' if it wasn't
        inserted,
        And raises TypeError if 'cls' isn't
        a class or if 'id' isn't a str.
        """
        target = BaseModel()
        self.storage.new(target)
        self.assertEqual(target, self.storage.get(BaseModel, target.id))

        self.assertIsNone(self.storage.get(Amenity, target.id))
        self.assertIsNone(self.storage.get(BaseModel, '<wrong id format>'))

        with self.assertRaises(TypeError):
            self.storage.get(5, None)
        with self.assertRaises(TypeError):
            self.storage.get(Place, 3.14)

        self.storage.delete(target)
        # delete the object to prevent conflict
        # with future tests
        self.assertEqual({}, self.storage.all())
        self.storage.save()

    def test_count(self):
        """
        Tests that 'FileStorage.count' counts
        all instances of 'cls', or returns the
        correct amount of objects in 'storage.all()'
        when 'cls' is None,

        and that 'FileStorage.count' raises 'TypeError'
        if 'cls' isn't a class.
        """
        target_base_model = BaseModel()
        target_amenity = Amenity(name="tv")
        target_state = State(name="California")

        self.storage.new(target_base_model)
        self.storage.new(target_amenity)
        self.storage.new(target_state)

        self.assertEqual(1, self.storage.count(BaseModel))
        self.assertEqual(1, self.storage.count(Amenity))
        self.assertEqual(1, self.storage.count(State))

        self.assertEqual(0, self.storage.count(Place))
        self.assertEqual(0, self.storage.count(Review))
        self.assertEqual(0, self.storage.count(User))

        self.assertEqual(3, self.storage.count())
        self.assertEqual(3, self.storage.count(None))

        with self.assertRaises(TypeError):
            self.storage.count(complex())
            self.storage.count(True)
            self.storage.count("")

        self.storage.delete(target_state)
        self.storage.delete(target_amenity)
        self.storage.delete(target_base_model)
        # delete the object to prevent conflict
        # with future tests
        self.assertEqual({}, self.storage.all())
        self.storage.save()

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
