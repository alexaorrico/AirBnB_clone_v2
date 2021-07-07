#!/usr/bin/python3
"""
Contains the TestFileStorageDocs classes
"""
from models import storage
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

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_reload(self):
        """Test that reload properly reload objects to __objects"""
        storage = FileStorage()
        state1 = State(name="California")
        storage.new(state1)
        storage.save()
        storage.reload()
        dic = storage.all(State)
        bool = False
        for k, v in dic.items():
            if v.name == 'California':
                bool = True
        self.assertEqual(bool, True)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_delete(self):
        """Test if objs will delete when delete method is called"""
        storage = FileStorage()
        city1 = City(name="SF")
        storage.new(city1)
        storage.reload()
        all_cities = storage.all(City).values()
        bool = False
        for obj in all_cities:
            if obj.name == 'SF':
                storage.delete(obj)
                bool = True
        self.assertEqual(bool, True)

        all_cities = storage.all(City).values()
        for obj in all_cities:
            if obj.name == "SF":
                bool = False
        self.assertEqual(bool, True)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_close(self):
        """Test close"""
        storage = FileStorage()
        amenity1 = Amenity(name="WIFI SERVICE")
        storage.new(amenity1)
        storage.save()
        exists = os.path.isfile('file.json')
        self.assertEqual(True, exists)
        storage.reload()
        dic = storage.all(State)
        bool = True
        for obj in dic.values():
            if obj.name == 'WIFI SERVICE':
                bool = False
        self.assertEqual(bool, True)
        storage.close()

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_get(self):
        """test get function"""
        first_state_id = list(storage.all("State").values())[0].id
        obj = storage.get("State", first_state_id)
        self.assertTrue(obj.__class__.__name__, "State")
        self.assertTrue(obj.id, first_state_id)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_count(self):
        """test count function"""
        count_state = storage.count("State")
        count_city = storage.count("City")
        count_place = storage.count("Place")
        count_review = storage.count("Review")
        count_user = storage.count("User")
        count_am = storage.count("Amenity")
        count = storage.count()
        self.assertTrue(count >= count_state, True)
        self.assertTrue(count >= count_city, True)
        self.assertTrue(count >= count_place, True)
        self.assertTrue(count >= count_review, True)
        self.assertTrue(count >= count_user, True)
        self.assertTrue(count >= count_am, True)
