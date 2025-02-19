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


class TestDBStorage(unittest.TestCase):
    """Test the DBStorage class"""

    @classmethod
    def setUpClass(cls):
        """Set up a test instance"""
        cls.storage = DBStorage()
        cls.storage.reload()

        # Create test objecs
        cls.user = User(email="test@example.com", password="test")
        cls.state = State(name="California")

        cls.storage.new(cls.user)
        cls.storage.new(cls.state)
        cls.storage.save()

        @classmethod
        def tearDownClass(cls):
            """Clean up test objects"""
            cls.storage.delete(cls.user)
            cls.storage.delete(cls.state)
            cls.storage.save()

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIsInstance(models.storage.all(), dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""
        all_objs = model.storage.all()
        self.assertGreaterEqual(len(all_objs), 2)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """test that new adds an object to the database"""
        new_city = City(name="New York")
        models.storage.new(new_city)
        models.storage.save()
        self.assertIn(f"City.{new_city.id}", models.storage.all())

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to database"""
        new_place = Place(name="Cool Place")
        models.storage.new(new_place)
        models.storage.save()
        self.assertIn(f"Place.{new_place.id}", models.storage.all())

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get_existing_object(self):
        """Test get method retrieves an existing object"""
        user = models.storage.get(User, self.user.id)
        self.assertIsNotNone(user)
        self.assertEqual(user.id, self.user.id)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get_nonexistent_object(self):
        """Test get method returns None for a non-existent object"""
        self.assertIsNone(models.storage.get(User, "nonexistent_id"))

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get_invalid_class(self):
        """Test get method returns None for an invalid class"""
        self.assertIsNone(models.storage.get("AClass", "1234"))

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count_all(self):
        """Test count method returns the total number of objects"""
        initial_count = models.storage.count()
        self.assertGreaterEqual(initial_count, 2)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count_specific_class(self):
        """Test count method returns correct count for a given class"""
        user_count = models.storage.count(User)
        state_count = models.storage.count(State)
        self.assertGreaterEqual(user_count, 1)
        self.assertGreaterEqual(state_count, 1)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count_invalid_class(self):
        """Test count method returns 0 for an invalid class"""
        self.assertEqual(models.storage.count("InvalidClass"), 0)


if __name__ == "__main__":
    unittest.main()
