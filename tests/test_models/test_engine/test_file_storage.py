#!/usr/bin/python3
"""
Contains the TestFileStorageDocs classes
"""

from datetime import datetime
import inspect
import unittest
import models
from unittest.mock import patch, Mock
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
    @patch.object(models.storage, 'all')
    def test_get(self, mock_all):
        """Test that get retrieve one object"""
        mock_user = Mock(spec=classes.get('State'))
        mock_user.id = '1234567890'
        cls = mock_user.__class__

        # All returns a dictionary containing object
        mock_all.return_value = {f'{cls.__name__}.{mock_user.id}': mock_user}
        obj = models.storage.get(cls, mock_user.id)
        mock_all.assert_called_once_with(cls)
        # Test that the object returned matches with the expected object
        self.assertEqual(mock_user, obj)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    @patch.object(models.storage, 'all')
    def test_count_cls_not_none(self, mock_all):
        """Test that count returns 1 when class and ID is passed
        with total object in database of type Place (1)
        """
        mock_place = Mock(spec=classes.get('Place'))
        mock_place.id = '1234567890'
        cls = mock_place.__class__

        # All returns a dictionary containing a single Place object
        mock_all.return_value = {f'{cls.__name__}.{mock_place.id}': mock_place}

        count = models.storage.count(cls)
        mock_all.assert_called_once_with(cls)

        self.assertEqual(count, 1)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    @patch.object(models.storage, 'all')
    def test_count_cls_none(self, mock_all):
        """Test that count returns 2 when None is passed or cls is empty
        with total object in the daabase of type Place and State (2)
        """
        mock_place = Mock(spec=classes.get('Place'))
        mock_state = Mock(spec=classes.get('State'))

        mock_place.id = '1234567890'
        mock_state.id = '0987654321'

        place_cls = mock_place.__class__
        state_cls = mock_state.__class__

        # All returns a dictionary containing a Place and State object
        mock_all.return_value = {
            f'{place_cls.__name__}.{mock_place.id}': mock_place,
            f'{state_cls.__name__}.{mock_state.id}': mock_state
        }
        count = models.storage.count(None)
        mock_all.assert_called_once_with(None)

        self.assertEqual(count, 2)
