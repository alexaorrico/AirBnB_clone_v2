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


@unittest.skipIf(STORAGE_TYPE != 'db', 'skip if environ is not db')
class TestCountGet(unittest.TestCase):
    """testing Count and Get methods"""

    @classmethod
    def setUpClass(cls):
        """sets up the class for this round of tests"""
        print('\n\n....................................')
        print('.......... Testing DBStorage .......')
        print('. State, City, User, Place Amenity .')
        print('....................................')
        storage.delete_all()
        cls.s = State(name="California")
        cls.c = City(state_id=cls.s.id,
                     name="San Francisco")
        cls.u = User(email="betty@holbertonschool.com",
                     password="pwd")
        cls.p1 = Place(user_id=cls.u.id,
                       city_id=cls.c.id,
                       name="a house")
        cls.p2 = Place(user_id=cls.u.id,
                       city_id=cls.c.id,
                       name="a house two")
        cls.a1 = Amenity(name="Wifi")
        cls.a2 = Amenity(name="Cable")
        cls.a3 = Amenity(name="Bucket Shower")
        objs = [cls.s, cls.c, cls.u, cls.p1, cls.p2, cls.a1, cls.a2, cls.a3]
        for obj in objs:
            obj.save()

    def setUp(self):
        """initializes new user for testing"""
        self.s = TestCountGet.s
        self.c = TestCountGet.c
        self.u = TestCountGet.u
        self.p1 = TestCountGet.p1
        self.p2 = TestCountGet.p2
        self.a1 = TestCountGet.a1
        self.a2 = TestCountGet.a2
        self.a3 = TestCountGet.a3

    def test_all_reload_save(self):
        """... checks if all(), save(), and reload function
        in new instance.  This also tests for reload"""
        actual = 0
        db_objs = storage.all()
        for obj in db_objs.values():
            for x in [self.s.id, self.c.id, self.u.id, self.p1.id]:
                if x == obj.id:
                    actual += 1
        self.assertTrue(actual == 4)

    def test_get_pace(self):
        """... checks if get() function returns properly"""
        duplicate = storage.get('Place', self.p1.id)
        expected = self.p1.id
        self.assertEqual(expected, duplicate.id)


    def test_count_all(self):
        """... checks if count() functions with no class"""
        count_all = storage.count()
        expected = 8
        self.assertEqual(expected, count_all)

if __name__ == '__main__':
    unittest.main
