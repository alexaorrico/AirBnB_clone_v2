#!/usr/bin/python3
"""
Contains the TestFileStorageDocs classes

    you may have to put this line to restart the app
    from models import storage
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
    def test_z00_count(self):
        """Test Returns the object based on the class and its ID,
        or None if not found"""
        from models import storage
        no_output = " > /dev/null 2>&1"
        str_cmd = 'echo \'create State name="Arizona"\' | ./console.py'

        os.system("rm file.json")

        code = os.system(str_cmd + no_output)
        self.assertFalse(code)

        storage.reload()
        num_states = storage.count(State)
        self.assertEqual(num_states, 1)

        os.system("rm file.json" + no_output)

    def test_z01_count_exception(self):
        """ test raises many arguments """
        from models import storage
        with self.assertRaises(TypeError):
            storage.count(State, City)
        with self.assertRaises(TypeError):
            storage.count(State, City, User)
        with self.assertRaises(TypeError):
            storage.count(State, City, User, Place)

    def test_z02_count_with_numbers(self):
        """ test count with numbers """
        from models import storage
        self.assertFalse(storage.count(20))
        self.assertFalse(storage.count(202))
        self.assertFalse(storage.count(20.20))
        self.assertFalse(storage.count(50.5))

    def test_z01_count_with_str(self):
        """ test count with str """
        from models import storage
        self.assertFalse(storage.count("State"))
        self.assertFalse(storage.count("User"))
        self.assertFalse(storage.count("Hola"))
        self.assertFalse(storage.count("hjssksksuisissj"))

    @unittest.skipIf(models.storage_t == 'db', "not testing db storage")
    def test_z10_get(self):
        """Test returns the number of objects in storage"""
        from models import storage
        no_output = " > /dev/null 2>&1"
        str_cmd = 'echo \'create State name="Arizona"\' | ./console.py'

        os.system("rm file.json" + no_output)

        code = os.system(str_cmd + no_output)
        self.assertFalse(code)

        first_state_id = list(storage.all(State).values())[0].id

        state = storage.get(State, first_state_id)
        self.assertTrue(state)
        self.assertEqual(state.id, first_state_id)

        os.system("rm file.json" + no_output)

    def test_z10_get(self):
        """Test empty file"""
        from models import storage
        no_output = " > /dev/null 2>&1"

        os.system("rm file.json" + no_output)

        state = storage.get(State, "FAKE_ID")
        self.assertEqual(state, None)

    def test_z11_get(self):
        """Test no valid class"""
        from models import storage
        no_output = " > /dev/null 2>&1"

        os.system("rm file.json" + no_output)

        state = storage.get("FAKE_CLASS", "FAKE_ID")
        self.assertEqual(state, None)
