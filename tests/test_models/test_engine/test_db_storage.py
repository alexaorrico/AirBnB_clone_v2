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
import MySQLdb
DBStorage = db_storage.DBStorage
storage = DBStorage()
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(
            ['tests/test_models/test_engine/test_db_storage.py'])
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

    def test_file_is_executable(self):
        """... tests if file has correct permissions so user can execute"""
        file_stat = os.stat('models/engine/db_storage.py')
        permissions = str(oct(file_stat[0]))
        actual = int(permissions[5:-2]) >= 5
        self.assertTrue(actual)


class TestFileStorage(unittest.TestCase):
    @classmethod
    def setUp(self):
        """Create the MySQLdb instantation"""
        storage.reload()

    @classmethod
    def tearDown(self):
        """Tear down the MySQLdb"""
        storage.close()

    """Test the FileStorage class"""

	@unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(models.storage.all()), dict)

	@unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""

    def test_state_no_name(self):
        """... checks to create a state with no name"""
        with self.assertRaises(Exception) as context:
            s = State()
            s.save()
        self.assertTrue('"Column \'name\' cannot be null"'
                        in str(context.exception))

    def test_city_no_state(self):
        """... checks to create a city with invalid state"""
        with self.assertRaises(Exception) as context:
            c = City(name="Tapioca", state_id="NOT VALID")
            c.save()
        self.assertTrue('a child row: a foreign key constraint fails'
                        in str(context.exception))

    def test_place_no_user(self):
        """... checks to create a place with no city"""
        with self.assertRaises(Exception) as context:
            p = Place()
            p.save()
        self.assertTrue('"Column \'city_id\' cannot be null"'
                        in str(context.exception))

    def test_review_no_text(self):
        """... checks to create a Review with no text"""
        with self.assertRaises(Exception) as context:
            r = Review()
            r.save()
        self.assertTrue('"Column \'text\' cannot be null"'
                        in str(context.exception))

    def test_amenity_no_name(self):
        """... checks to create an amenity with no name"""
        with self.assertRaises(Exception) as context:
            a = Amenity()
            a.save()
        self.assertTrue('"Column \'name\' cannot be null"'
                        in str(context.exception))

    def test_user_no_name(self):
        """... checks to create a user with no email"""
        with self.assertRaises(Exception) as context:
            u = User()
            u.save()
        self.assertTrue('"Column \'email\' cannot be null"'
                        in str(context.exception))
	
	@unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """test that new adds an object to the database"""

	@unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""

    def test_get(self):
        """testing the method get"""
        q1 = State(name='Trial')
        storage.new(q1)
        storage.save()
        q2 = storage.get("State", q1.id)
        self.assertTrue(q2)

    def test_count(self):
        """Test count method"""
        count_a = storage.count()
        q1 = State(name='Trial')
        storage.new(q1)
        storage.save()
        count_b = storage.count()
        self.assertNotEqual(count_a, count_b)


if __name__ == '__main__':
    unittest.main
