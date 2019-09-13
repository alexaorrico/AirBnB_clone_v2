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
import pep8
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

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
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
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(models.storage.all()), dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """test that new adds an object to the database"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_db_get(self):
        """Test for get request"""
        s = State(name="test_state_please_delete")
        s.save()
        self.assertEqual(models.storage.get("State", s.id), s)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_dbs_count(self):
        """test for count request"""
        count = models.storage.count("State")
        s = State(name="test_state_please_delete")
        s.save()
        self.assertEqual(models.storage.count("State"), count + 1)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_delete_user_and_its_place_and_review(self):
        """tests deleting a user associated with a place"""
        from models import storage
        n = str(randint(0, 100))
        s = State(name="TestState" + n)
        s.save()
        c = City(name="TestCity" + n, state_id=s.id)
        c.save()
        u = User(name="TestUser" + n, email="foo" + n, password="bar")
        u.save()
        p = Place(name="TestPlace" + n, city_id=c.id, user_id=u.id)
        p.save()
        r = Review(text="TestReview" + n, place_id=p.id, user_id=u.id)
        r.save()
        storage.delete(u)
        storage.save()
        city_key = "City." + c.id
        state_key = "State." + c.id
        user_key = "User." + u.id
        place_key = "Place." + p.id
        self.assertFalse(user_key in storage.all(User))
        self.assertFalse(place_key in storage.all(Place))
        self.assertTrue(state_key in storage.all(City))
        self.assertTrue(city_key in storage.all(State))
        self.assertFalse(("Review." + r.id) in storage.all(Place))

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_delete_place(self):
        """test deleting the user of a place"""
        from models import storage
        n = str(randint(0, 100))
        s = State(name="TestState" + n)
        s.save()
        c = City(name="TestCity" + n, state_id=s.id)
        c.save()
        u = User(name="TestUser" + n, email="foo" + n, password="bar")
        u.save()
        p = Place(name="TestPlace" + n, city_id=c.id, user_id=u.id)
        p.save()
        storage.delete(p)
        storage.save()
        self.assertTrue(("User." + u.id) in storage.all(User))
        self.assertFalse(("Place." + p.id) in storage.all(Place))

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_delete_place_with_review(self):
        """test deleting a place and its review """
        from models import storage
        n = str(randint(0, 100))
        s = State(name="TestState" + n)
        s.save()
        c = City(name="TestCity" + n, state_id=s.id)
        c.save()
        u = User(name="TestUser" + n, email="foo" + n, password="bar")
        u.save()
        p = Place(name="TestPlace" + n, city_id=c.id, user_id=u.id)
        p.save()
        r = Review(text="TestReview" + n, place_id=p.id, user_id=u.id)
        r.save()
        storage.delete(p)
        storage.save()
        self.assertTrue(("User." + u.id) in storage.all(User))
        self.assertFalse(("Place." + p.id) in storage.all(Place))
        self.assertFalse(("Review." + r.id) in storage.all(Review))
