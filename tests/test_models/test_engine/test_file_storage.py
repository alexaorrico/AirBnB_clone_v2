#!/usr/bin/python3
"""
Contains the TestFileStorageDocs classes
"""

from datetime import datetime
import inspect
import json
import os
import pep8
import unittest
import models
from models.__init__ import storage
from models.engine import file_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

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

    # def setUp(self):
    #     """Set up test environment"""
    #     del_list = []
    #     for key in storage._FileStorage__objects.keys():
    #         del_list.append(key)
    #     for key in del_list:
    #         del storage._FileStorage__objects[key]

    # def tearDown(self):
    #     """Remove storage file at end of tests"""
    #     try:
    #         os.remove("file.json")
    #     except FileNotFoundError:
    #         pass

    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.fs_f = inspect.getmembers(FileStorage, inspect.isfunction)

    # @classmethod
    # def tearDownClass(cls):
    #     """Rmove file"""
    #     try:
    #         os.remove("file.json")
    #     except Exception:
    #         pass

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
        msg = "FileStorage class needs a docstring"
        self.assertIsNot(
            FileStorage.__doc__, None, msg
        )
        self.assertTrue(
            len(FileStorage.__doc__) >= 1, msg
        )

    def test_fs_func_docstrings(self):
        """Test for the presence of docstrings in FileStorage methods"""
        for func in self.fs_f:
            output = "{:s} method needs a docstring".format(func[0])
            self.assertIsNot(
                func[1].__doc__, None, output
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

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_get(self):
        """Test that get returns only one instance if found"""
        storage = FileStorage()
        FileStorage._FileStorage__objects = {}
        from console import HBNBCommand
        from unittest.mock import patch
        from io import StringIO
        console = HBNBCommand()
        for cls in classes.values():
            with self.subTest(cls=cls):
                with patch("sys.stdout", new=StringIO()) as output:
                    console.onecmd('create {}'.format(cls))
                    print(output, 'console output')
        # storage.reload()
        # for cls in classes.values():
            # with self.subTest(cls=cls):
            #     first_id = list(storage.all(cls).values())[0].id
            #     output = str(storage.get(cls, first_id))
            #     print(output,'output ffffffffffff')
            #     self.assertIn(first_id, output)

    @unittest.skipIf(models.storage_t == "db", "not testint db storage")
    def test_count_without_data(self):
        """Test count return the number of objects"""
        storage = FileStorage()
        FileStorage._FileStorage__objects = {}
        self.assertEqual(len(storage.all()), 0)
