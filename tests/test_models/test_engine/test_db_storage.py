#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
import models
from models.engine import db_storage
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
DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pycodestyle_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pycodestyles = pycodestyle.StyleGuide(quiet=True)
        result = pycodestyles.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pycodestyle_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pycodestyles = pycodestyle.StyleGuide(quiet=True)
        result = pycodestyles.check_files(['tests/test_models/test_engine/\
test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""
    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
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
        self.assertEqual(None, models.storage.get(int, "dksfjsd"))
        self.assertEqual(newCity, models.storage.get(City, newCity.id))
        self.assertEqual(newUser, models.storage.get(User, newUser.id))
        self.assertEqual(newPlace, models.storage.get(Place, newPlace.id))
        self.assertEqual(newReview, models.storage.get(Review, newReview.id))
        self.assertEqual(newAmenity,
                         models.storage.get(Amenity, newAmenity.id))
        self.assertEqual(None, models.storage.get(State, "Not a good ID"))

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
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
