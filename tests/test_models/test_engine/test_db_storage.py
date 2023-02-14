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
from random import randint
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
    def test_dbs_get_method(self):
        """Test for get nethod"""
        s = State(name="Florida")
        s.save()
        self.assertEqual(models.storage.get("State", s.id), s)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_dbs_count_method(self):
        """test for count method"""
        count = models.storage.count("State")
        s = State(name="Florida")
        s.save()
        self.assertEqual(models.storage.count("State"), count + 1)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_delete_user_with_place_and_review(self):
        """tests deleting a user associated with a place"""
        from models import storage
        n = str(randint(0, 100))
        s = State(name="Kali" + n)
        s.save()
        c = City(name="Frisco" + n, state_id=s.id)
        c.save()
        u = User(name="Userio" + n, email="foo" + n, password="bar")
        u.save()
        p = Place(name="Housy" + n, city_id=c.id, user_id=u.id)
        p.save()
        r = Review(text="Great!" + n, place_id=p.id, user_id=u.id)
        r.save()
        storage.delete(u)
        storage.save()
        user_key = "User." + u.id
        place_key = "Place." + p.id
        self.assertFalse(user_key in storage.all(User))
        self.assertFalse(place_key in storage.all(Place))
        self.assertFalse(("Review." + r.id) in storage.all(Place))

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_delete_place(self):
        """tests deleting a user associated with a place"""
        from models import storage
        n = str(randint(0, 100))
        s = State(name="Kali" + n)
        s.save()
        c = City(name="Frisco" + n, state_id=s.id)
        c.save()
        u = User(name="Userio" + n, email="foo" + n, password="bar")
        u.save()
        p = Place(name="Housy" + n, city_id=c.id, user_id=u.id)
        p.save()
        storage.delete(p)
        storage.save()
        self.assertTrue(("User." + u.id) in storage.all(User))
        self.assertFalse(("Place." + p.id) in storage.all(Place))

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_delete_place_with_review(self):
        """tests deleting a user associated with a place"""
        from models import storage
        n = str(randint(0, 100))
        s = State(name="Kali" + n)
        s.save()
        c = City(name="Frisco" + n, state_id=s.id)
        c.save()
        u = User(name="Userio" + n, email="foo" + n, password="bar")
        u.save()
        p = Place(name="Housy" + n, city_id=c.id, user_id=u.id)
        p.save()
        r = Review(text="Great!" + n, place_id=p.id, user_id=u.id)
        r.save()
        storage.delete(p)
        storage.save()
        self.assertTrue(("User." + u.id) in storage.all(User))
        self.assertFalse(("Place." + p.id) in storage.all(Place))
        self.assertFalse(("Review." + r.id) in storage.all(Review))

    """
    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get_amenites_from_place(self):
        gets all amenities
        from models import storage
        import requests
        n = str(randint(0, 100))
        s = State(name="Kali" + n)
        s.save()
        c = City(name="Frisco" + n, state_id=s.id)
        c.save()
        u = User(name="Userio" + n, email="foo" + n, password="bar")
        u.save()
        p = Place(name="Housy" + n, city_id=c.id, user_id=u.id)
        p.save()
        a = Amenity(name="SuperWIFI" + n)
        a.save()
        p.amenities.append(a)
        p.save()

        url = "http://localhost:5000/api/v1/places/{}/amenities".format(p.id)
        r = requests.get(url)
        self.assertTrue(r is not None)
        self.assertEqual(r.status_code, 200)
        self.assertIn(a.id, [d["id"] for d in r.json()])
    """
