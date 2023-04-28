#!/usr/bin/python3
"""
Contains the TestFileStorageDocs classes
"""

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
from io import StringIO
from tests import reset_stream
from unittest.mock import patch
from console import HBNBCommand
import json
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

    @unittest.skipIf(models.storage_t == 'db', "not testing db storage")
    def test_get_valid_class(self):
        """Test the `get` method using a `State` object"""
        with patch('sys.stdout', new=StringIO()) as fd:
            # get existing number of objects of given class
            old_len = len(list(models.storage.all(State).values()))

            # create new `State` object
            HBNBCommand().onecmd('create State name="Imo"')
            id = fd.getvalue().strip()
            reset_stream(fd)

            new_len = len(list(models.storage.all(State).values()))
            self.assertEqual(old_len + 1, new_len)

            # test `get` method
            objs = models.storage.all(State).values()
            obj = None
            for obj in objs:
                if obj.id == id:
                    break

            self.assertNotEqual(obj, None)

            our_state = models.storage.get(State, id)
            self.assertEqual(our_state.name, obj.name)
            self.assertEqual(our_state.id, obj.id)
            self.assertEqual(our_state, obj)

    @unittest.skipIf(models.storage_t == 'db', "not testing db storage")
    def test_get_invalid_id(self):
        """Test the `get` method using an invalid id"""
        with patch('sys.stdout', new=StringIO()) as fd:
            # create new object
            HBNBCommand().onecmd('create State name="Imo"')
            id = fd.getvalue().strip()
            reset_stream(fd)

            our_state = models.storage.get(State, id + "z")
            self.assertEqual(our_state, None)

    @unittest.skipIf(models.storage_t == 'db', "not testing db storage")
    def test_get_exceptions(self):
        """Test the `get` method to raise exceptions"""
        with self.assertRaises(TypeError):
            models.storage.get("Invalid", "id")

        with self.assertRaises(TypeError):
            models.storage.get(State, 10)

    @unittest.skipIf(models.storage_t == 'db', "not testing db storage")
    def test_count_class(self):
        """Test the count method for the `User` class"""
        with patch('sys.stdout', new=StringIO()) as fd:
            old_count = models.storage.count(User)

            # create new object
            HBNBCommand().onecmd(
                'create User email="nil@nil.com" password="nil"')
            reset_stream(fd)

            new_count = models.storage.count(User)
            self.assertEqual(old_count + 1, new_count)

    @unittest.skipIf(models.storage_t == 'db', "not testing db storage")
    def test_count_all(self):
        """Test the `count` method for all classes"""
        with patch('sys.stdout', new=StringIO()) as fd:
            old_count = models.storage.count()

            # create new object
            HBNBCommand().onecmd(
                'create User email="nil@nil.com" password="nil"')
            reset_stream(fd)

            new_count = models.storage.count()
            self.assertEqual(old_count + 1, new_count)

    @unittest.skipIf(models.storage_t == 'db', "not testing db storage")
    def test_count_exceptions(self):
        """Test the `get` method to raise exceptions"""
        with self.assertRaises(TypeError):
            models.storage.count("Invalid class")
