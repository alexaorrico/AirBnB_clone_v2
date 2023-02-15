#!/usr/bin/python3
"""Unittests for testing models/engine/db_storage.py."""
import os
import pep8
import inspect
import unittest
import MySQLdb
import models
from models.engine.db_storage import DBStorage
from models.state import State
from models.user import User


class TestDBStorageDocs(unittest.TestCase):
    """Test documentation and style."""

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
        self.assertIsNot(DBStorage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
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
        """Instantiate MySQLdb cursor."""
        if type(models.storage) == DBStorage:
            db = MySQLdb.connect(user=os.getenv("HBNB_MYSQL_USER"),
                                 passwd=os.getenv("HBNB_MYSQL_PWD"),
                                 db=os.getenv("HBNB_MYSQL_DB"))
            cls.cursor = db.cursor()
            cls.storage = DBStorage()
            cls.storage.reload()
            cls.state = State(name="California")
            cls.user = User(email="holberton@holberton.com",
                            password="password")
            cls.storage._DBStorage__session.add(cls.state)
            cls.storage._DBStorage__session.add(cls.user)
            cls.storage._DBStorage__session.commit()

    @classmethod
    def tearDownClass(cls):
        """Close MySQLdb cursor."""
        if type(models.storage) == DBStorage:
            cls.cursor.close()
            cls.storage._DBStorage__session.close()

    @unittest.skipIf(models.storage_t != "db", "not testing file storage")
    def test_all_no_class(self):
        """Test all method without a specified class."""
        objs = models.storage.all()
        self.assertEqual(type(objs), dict)
        self.assertEqual(len(objs), 2)

    @unittest.skipIf(models.storage_t != "db", "not testing file storage")
    def test_all_specified_class(self):
        """Test all method with specified class."""
        users = self.storage.all(User)
        self.assertEqual(len(users), 1)
        self.assertEqual(list(users.values())[0].email,
                         "holberton@holberton.com")

    @unittest.skipIf(models.storage_t != "db", "not testing file storage")
    def test_new(self):
        """Test new method."""
        ny = State(name="New York")
        self.storage.new(ny)
        self.assertIn(ny, list(self.storage._DBStorage__session.new))
        self.storage._DBStorage__session.rollback()

    @unittest.skipIf(models.storage_t != "db", "not testing file storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""
        ak = State(name="Arkansas")
        self.storage._DBStorage__session.add(ak)
        self.storage.save()
        self.cursor.execute("SELECT * FROM states WHERE name = 'Arkansas'")
        query = self.cursor.fetchall()
        self.assertEqual(ak.id, query[0][0])
        self.cursor.execute("DELETE FROM states WHERE name = 'Arkansas'")

    @unittest.skipIf(models.storage_t != "db", "not testing file storage")
    def test_get(self):
        """Test get method."""
        self.assertEqual(self.storage.get("User", self.user.id), self.user)

    @unittest.skipIf(models.storage_t != "db", "not testing file storage")
    def test_get_nonexistant(self):
        """Test get method with nonexistant object."""
        self.assertIsNone(self.storage.get("User", "nonexistant"))

    @unittest.skipIf(models.storage_t != "db", "not testing file storage")
    def test_count_no_class(self):
        """Test count method without specified class."""
        self.assertEqual(2, self.storage.count())

    @unittest.skipIf(models.storage_t != "db", "not testing file storage")
    def test_count_specified_class(self):
        """Test count method with specified class."""
        self.assertEqual(1, self.storage.count("User"))
