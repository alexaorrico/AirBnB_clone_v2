#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
import models
import MySQLdb
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
if os.getenv("HBNB_TYPE_STORAGE") == 'db':
    my_db = MySQLdb.connect(host=os.getenv("HBNB_MYSQL_HOST"),
                            port=3306,
                            user=os.getenv("HBNB_MYSQL_USER"),
                            password=os.getenv("HBNB_MYSQL_PWD"),
                            db=os.getenv("HBNB_MYSQL_DB"))
    cursor = my_db.cursor()


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
        SQL = "SELECT COUNT(name) FROM states"
        cursor.execute(SQL)
        count = int(cursor.fetchone()[0])
        my_db.commit()
        state = State(name="Kansas")
        state.save()
        cursor.execute(SQL)
        new_count = int(cursor.fetchone()[0])
        self.assertEqual(count + 1, new_count)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get(self):
        """Test that get retrieves the right objects from the database"""
        state = State(name="New York")
        state.save()
        amenity = Amenity(name="Garden")
        amenity.save()
        my_state = models.storage.get(State, state.id)
        self.assertEqual(state, my_state)
        my_amenity = models.storage.get("Amenity", amenity.id)
        self.assertEqual(amenity, my_amenity)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count_class(self):
        """test that count returns the right number of objects """
        state_count = models.storage.count(State)
        SQL = "SELECT COUNT(*) FROM states"
        cursor.execute(SQL)
        count = int(cursor.fetchone()[0])
        my_db.commit()
        self.assertEqual(state_count, count)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count_all(self):
        """test that count returns right object number when no class given"""
        count = 0
        my_classes = ["states", "cities", "amenities", "places", "users",
                      "reviews"]
        for clss in my_classes:
            SQL = "SELECT COUNT(*) FROM {}".format(clss)
            cursor.execute(SQL)
            count += int(cursor.fetchone()[0])
            my_db.commit()
        my_count = models.storage.count()
        self.assertEqual(count, my_count)
