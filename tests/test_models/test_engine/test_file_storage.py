#!/usr/bin/python3
"""
Contains the TestFileStorageDocs classes
"""

import inspect
import json
import os
import unittest
from datetime import datetime

import pycodestyle

from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.engine import file_storage
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

FileStorage = file_storage.FileStorage
classes = {
    "Amenity": Amenity, "BaseModel": BaseModel, "City": City,
    "Place": Place, "Review": Review, "State": State, "User": User
}


class TestFileStorageDocs(unittest.TestCase):
    """
    Tests to check the documentation and style of FileStorage class
    """

    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.fs_f = inspect.getmembers(FileStorage, inspect.isfunction)

    def test_pep8_conformance_file_storage(self):
        """Test that models/engine/file_storage.py conforms to PEP8."""
        pep8s = pycodestyle.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/file_storage.py'])
        self.assertEqual(
            result.total_errors,
            0,
            "Found code style errors (and warnings)."
        )

    def test_pep8_conformance_test_file_storage(self):
        """
        Test tests/test_models/test_file_storage.py conforms to PEP8.
        """
        pep8s = pycodestyle.StyleGuide(quiet=True)
        result = pep8s.check_files([
            'tests/test_models/test_engine/test_file_storage.py'
        ])
        self.assertEqual(
            result.total_errors,
            0,
            "Found code style errors (and warnings)."
        )

    def test_file_storage_module_docstring(self):
        """Test for the file_storage.py module docstring"""
        self.assertIsNot(file_storage.__doc__, None,
                         "file_storage.py needs a docstring")
        self.assertTrue(
            len(file_storage.__doc__) >= 1,
            "file_storage.py needs a docstring"
        )

    def test_file_storage_class_docstring(self):
        """Test for the FileStorage class docstring"""
        self.assertIsNot(
            FileStorage.__doc__,
            None,
            "FileStorage class needs a docstring"
        )
        self.assertTrue(
            len(FileStorage.__doc__) >= 1,
            "FileStorage class needs a docstring"
        )

    def test_fs_func_docstrings(self):
        """Test for the presence of docstrings in FileStorage methods"""
        for func in self.fs_f:
            self.assertIsNot(
                func[1].__doc__,
                None,
                "{:s} method needs a docstring".format(func[0])
            )
            self.assertTrue(
                len(func[1].__doc__) >= 1,
                "{:s} method needs a docstring".format(func[0])
            )


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""

    @unittest.skipIf(
        file_storage.is_db == True,
        "not testing file storage"
    )
    def test_all_returns_dict(self):
        """Test that all returns the FileStorage.__objects attr"""
        storage = FileStorage()
        new_dict = storage.all()
        self.assertEqual(type(new_dict), dict)
        self.assertIs(new_dict, storage._FileStorage__objects)

    @unittest.skipIf(
        file_storage.is_db == True,
        "not testing file storage"
    )
    def test_new(self):
        """
