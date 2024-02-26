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


class TestFileStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of FileStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.fs_f = inspect.getmembers(FileStorage, inspect.isfunction)

    def test_pycodestyle_conformance_file_storage(self):
        """Test that models/engine/file_storage.py conforms to PEP8."""
        pycodestyles = pycodestyle.StyleGuide(quiet=True)
        result = pycodestyles.check_files(['models/engine/file_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pycodestyle_conformance_test_file_storage(self):
        """Test tests/test_models/test_file_storage.py conforms to PEP8."""
        pycodestyles = pycodestyle.StyleGuide(quiet=True)
        result = pycodestyles.check_files(['tests/test_models/test_engine/\
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
    def setUp(self):
        """ Set up test environment """
        del_list = []
        for key in models.storage._FileStorage__objects.keys():
            del_list.append(key)
        for key in del_list:
            del models.storage._FileStorage__objects[key]

    def tearDown(self):
        """ Remove storage file at end of tests """
        try:
            os.remove('file.json')
        except Exception:
            pass

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
    def test_get(self):
        """Testing the get methods from the db storage"""
        newState = State(name="California")
        newCity = City(name="San_Francisco", state_id=newState.id)
        newUser = User(email="thisisanemail@email.com",
                       password="thisisnotapassword")
        newPlace = Place(name="Great Five Stars Hotel",
                         city_id=newCity.id,
                         state_id=newState.id,
                         user_id=newUser.id)
        newReview = Review(text="This is a review",
                           place_id=newPlace.id,
                           user_id=newUser.id)
        newAmenity = Amenity(name="Ventilator3000")
        newState.save()
        newCity.save()
        newUser.save()
        newPlace.save()
        newReview.save()
        newAmenity.save()
        self.assertEqual(None, models.storage.get("jkdsf", "dksfjsd"))
        self.assertEqual(newCity, models.storage.get(City, newCity.id))
        self.assertEqual(newUser, models.storage.get(User, newUser.id))
        self.assertEqual(newPlace, models.storage.get(Place, newPlace.id))
        self.assertEqual(newReview, models.storage.get(Review, newReview.id))
        self.assertEqual(newAmenity,
                         models.storage.get(Amenity, newAmenity.id))
        self.assertEqual(None, models.storage.get(State, "Not a good ID"))

    @unittest.skipIf(models.storage_t == 'db', "not testing db storage")
    def test_count(self):
        """testing the count function form the db storage"""
        currentNumberOfState = models.storage.count(State)
        listOfState = ["California", "New_York", "Floride", "Utah"]
        for stateName in listOfState:
            newState = State(name=stateName)
            newState.save()
        newNumberOfState = models.storage.count(State)
        self.assertEqual(newNumberOfState - currentNumberOfState,
                         len(listOfState))
        allInstance = models.storage.count()
        self.assertEqual(allInstance - currentNumberOfState,
                         len(listOfState))
        texasState = State(name="Texas")
        texasState.save()
        newNumberOfState += 1
        currentNumberOfCity = models.storage.count(City)
        listCityOfTexas = ["Austin", "Dallas", "Del Rio", "Killeen"]
        for cityName in listCityOfTexas:
            newCity = City(name=cityName, state_id=texasState.id)
            newCity.save()
        newNumberOfCity = models.storage.count(City)
        self.assertEqual(newNumberOfCity - currentNumberOfCity,
                         len(listCityOfTexas))
        allInstance = models.storage.count()
        numberOfState = newNumberOfState - currentNumberOfState
        numberOfCity = newNumberOfCity - currentNumberOfCity
        numberOfAllInstance = numberOfState + numberOfCity
        self.assertEqual(numberOfAllInstance, allInstance)
