#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
import models
from models.engine import db_storage
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import json
import os
import pep8
import unittest
DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class TestDBStorage(unittest.TestCase):
    """Test cases for DBStorage class"""

    @classmethod
    def setUpClass(cls):
        """Set up for the tests"""
        # Set environment variables for the test database
        os.environ['HBNB_MYSQL_USER'] = 'hbnb_test'
        os.environ['HBNB_MYSQL_PWD'] = 'hbnb_test_pwd'
        os.environ['HBNB_MYSQL_HOST'] = 'localhost'
        os.environ['HBNB_MYSQL_DB'] = 'hbnb_test_db'
        os.environ['HBNB_ENV'] = 'test'

        # Initialize the storage
        cls.storage = DBStorage()
        cls.storage.reload()

    @classmethod
    def tearDownClass(cls):
        """Tear down after the tests"""
        cls.storage._DBStorage__session.close()

    def setUp(self):
        """Set up for individual tests"""
        self.session = self.storage._DBStorage__session

    def tearDown(self):
        """Clean up after individual tests"""
        self.session.rollback()
        for table in reversed(Base.metadata.sorted_tables):
            self.session.execute(table.delete())
        self.session.commit()

    def test_all_returns_dict(self):
        """Test that all returns a dictionary"""
        self.assertIsInstance(self.storage.all(), dict)

    def test_new_adds_obj(self):
        """Test that new adds an object to the session"""
        user = User(email="test@test.com", password="test_pwd")
        self.storage.new(user)
        self.assertIn(user, self.session.new)

    def test_save_commits_session(self):
        """Test that save commits the session"""
        user = User(email="test@test.com", password="test_pwd")
        self.storage.new(user)
        self.storage.save()
        self.assertNotIn(user, self.session.new)

    def test_delete_removes_obj(self):
        """Test that delete removes an object from the session"""
        user = User(email="test@test.com", password="test_pwd")
        self.storage.new(user)
        self.storage.save()
        self.storage.delete(user)
        self.assertIn(user, self.session.deleted)

    def test_reload(self):
        """Test that reload recreates the session"""
        self.storage.reload()
        self.assertIsInstance(self.storage._DBStorage__session, Session)

    def test_all_with_class(self):
        """Test that all returns objects of a given class"""
        user1 = User(email="test1@test.com", password="test_pwd")
        user2 = User(email="test2@test.com", password="test_pwd")
        self.storage.new(user1)
        self.storage.new(user2)
        self.storage.save()
        users = self.storage.all(User)
        self.assertEqual(len(users), 2)
        self.assertIn(f"User.{user1.id}", users)
        self.assertIn(f"User.{user2.id}", users)

    def test_dbs_get(self):
        """Test DBStorage get method finds specified obj in storage"""
        obj = User()
        obj.save()
        self.assertEqual(self.storage.get(obj.__class__, obj.id), obj)


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


if __name__ == '__main__':
    unittest.main()
