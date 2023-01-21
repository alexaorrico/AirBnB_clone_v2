#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

import inspect
import unittest
from os import getenv

import MySQLdb
import pep8

import models
from models.amenity import Amenity
from models.city import City
from models.engine import db_storage
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

DBStorage = db_storage.DBStorage
classes = {
    "Amenity": Amenity,
    "City": City,
    "Place": Place,
    "Review": Review,
    "State": State,
    "User": User
}


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
        result = pep8s.check_files(
            ['tests/test_models/test_engine/\
test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(
            len(db_storage.__doc__) >= 1, "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(
            len(DBStorage.__doc__) >= 1, "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(
                len(func[1].__doc__) >= 1,
                "{:s} method needs a docstring".format(func[0]))


class TestDBStorage(unittest.TestCase):
    """Test the DBStorage class"""

    @classmethod
    def setUpClass(cls):
        """initial configuration for tests"""
        if (models.storage_t == 'db'):
            cls.conn = MySQLdb.connect(host=getenv("HBNB_MYSQL_HOST"),
                                       port=3306,
                                       user=getenv("HBNB_MYSQL_USER"),
                                       passwd=getenv("HBNB_MYSQL_PWD"),
                                       db=getenv("HBNB_MYSQL_DB"),
                                       charset="utf8")
            cls.cur = cls.conn.cursor()
            cls.storage = DBStorage()
            cls.storage.reload()

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionary"""
        self.cur.execute("""INSERT INTO `amenities` VALUES
            ('017ec502-e84a-4a0f-92d6-d97e27bc6bdf',
            '2017-03-25 02:17:06','2017-03-25 02:17:06','Cable TV')""")
        self.storage.reload()
        self.assertIs(type(self.storage.all(Amenity)), dict)
        self.assertGreaterEqual(len(self.storage.all()), 1)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""
        self.cur.execute("""INSERT INTO `amenities` VALUES
            ('017ec502-e84a-4a0f-92d6-d97e27cc6bdf',
            '2017-03-25 02:17:06','2017-03-25 02:17:06','Cable TV')""")
        self.storage.reload()
        self.assertIs(type(self.storage.all()), dict)
        self.assertGreaterEqual(len(self.storage.all()), 1)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """test that new adds an object to the database"""
        aminity = Amenity(name="Wi-Fi")
        self.storage.new(aminity)
        objs = self.storage.all(Amenity)
        self.assertIn(aminity, list(objs.values()))

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to the database"""
        aminity = Amenity(name="Wi-Fi")
        self.storage.new(aminity)
        self.storage.save()
        self.storage.reload()
        objs = self.storage.all(Amenity)
        self.assertIn("Amenity.{}".format(aminity.id), list(objs.keys()))

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get_with_cls(self):
        """Test that get properly gets an object with the given id and class"""
        obj_1 = Amenity(name="Wi-Fi")
        obj_2 = Amenity(name="TV")
        self.storage.new(obj_1)
        self.storage.new(obj_2)
        self.storage.save()
        self.storage.reload()

        found = self.storage.get(Amenity, obj_1.id)
        self.assertEqual(found.id, obj_1.id)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get_with_none(self):
        """Test that get returns None for object not found"""
        self.assertIsNone(self.storage.get(None, ""))
        self.assertIsNone(self.storage.get(Amenity, "abc"))

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count_with_cls(self):
        """Test that count returns the count of objs that match cls"""
        obj_1 = Amenity(name="Wi-Fi")
        obj_2 = Amenity(name="TV")
        self.storage.new(obj_1)
        self.storage.new(obj_2)
        self.storage.save()
        self.storage.reload()

        amenity_count = len(self.storage.all(Amenity))
        self.assertEqual(self.storage.count(Amenity), amenity_count)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count_all(self):
        """Test that count returns the count of all objs"""
        self.assertEqual(self.storage.count(), len(self.storage.all()))
