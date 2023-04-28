#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

import inspect
import models
from models.engine import db_storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from console import HBNBCommand
from tests import reset_stream
from io import StringIO
from unittest.mock import patch
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
    def test_get_valid_class(self):
        """Test the `get` method using a `State` object"""
        with patch('sys.stdout', new=StringIO()) as fd:
            # get existing number of objects of given class
            old_len = len(list(models.storage.all(State).values()))

            # create new `State` object
            HBNBCommand().onecmd('create State name="Imo"')
            id = fd.getvalue().strip()
            reset_stream(fd)

            new_len = len(list(models.storage.all(State).values()))
            self.assertEqual(old_len + 1, new_len)

            # test `get` method
            objs = models.storage.all(State).values()
            obj = None
            for obj in objs:
                if obj.id == id:
                    break

            self.assertNotEqual(obj, None)

            our_state = models.storage.get(State, id)
            self.assertEqual(our_state.name, obj.name)
            self.assertEqual(our_state.id, obj.id)
            self.assertEqual(our_state, obj)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get_invalid_id(self):
        """Test the `get` method using an invalid id"""
        with patch('sys.stdout', new=StringIO()) as fd:
            # create new object
            HBNBCommand().onecmd('create State name="Imo"')
            id = fd.getvalue().strip()
            reset_stream(fd)

            our_state = models.storage.get(State, id + "z")
            self.assertEqual(our_state, None)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get_exceptions(self):
        """Test the `get` method to raise exceptions"""
        with self.assertRaises(TypeError):
            models.storage.get("Invalid", "id")

        with self.assertRaises(TypeError):
            models.storage.get(State, 10)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count_class(self):
        """Test the count method for the `User` class"""
        with patch('sys.stdout', new=StringIO()) as fd:
            old_count = models.storage.count(User)

            # create new object
            HBNBCommand().onecmd(
                'create User email="nil@nil.com" password="nil"')
            reset_stream(fd)

            new_count = models.storage.count(User)
            self.assertEqual(old_count + 1, new_count)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count_all(self):
        """Test the `count` method for all classes"""
        with patch('sys.stdout', new=StringIO()) as fd:
            old_count = models.storage.count()

            # create new object
            HBNBCommand().onecmd(
                'create User email="nil@nil.com" password="nil"')
            reset_stream(fd)

            new_count = models.storage.count()
            self.assertEqual(old_count + 1, new_count)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count_exceptions(self):
        """Test the `get` method to raise exceptions"""
        with self.assertRaises(TypeError):
            models.storage.count("Invalid class")
