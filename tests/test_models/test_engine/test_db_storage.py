#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

import inspect
from os import getenv

import MySQLdb
import models
from models.base_model import Base
from models.engine import db_storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import pep8
import unittest
DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}

classes_test = {
    "User": {"first_name": "chuks", "last_name": "somzzy", "user_id": "save",
             "email": "somzzy@gmail.com", "password": "somzzy"},
    "State": {"name": "Lagos", "state_id": "save"},
    "City": {"name": "ojo", "state_id": None, "city_id": "save"},
    "Place": {"city_id": None, "user_id": None, "name":
              "Sheikh Murtadha str", "number_rooms": 3,
              "number_bathrooms": 2, "max_guest": 6,
              "price_by_night": 5000, "place_id": "save"},
    "Review": {"place_id": None, "user_id": None,
               "text": "Just Some test review", "review_id": "save"},
    "Amenity": {"name": "wifi", "amenity_id": "save"}
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
        if DBStorage.__doc__:
            self.assertTrue(len(DBStorage.__doc__) >= 1,
                            "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            if func[1].__doc__:
                self.assertTrue(len(func[1].__doc__) >= 1,
                                "{:s} method needs a docstring".
                                format(func[0]))


class TestDBStorage(unittest.TestCase):
    """Test the FileStorage class"""

    conn = None
    cur = None

    @classmethod
    def setUpClass(cls):
        """Setup for TestDBStorage"""
        if models.storage_t == "db" and getenv('HBNB_ENV') == "test":
            cls.conn = MySQLdb.connect(host=getenv('HBNB_MYSQL_HOST'),
                                       password=getenv('HBNB_MYSQL_PWD'),
                                       user=getenv('HBNB_MYSQL_USER'),
                                       database=getenv('HBNB_MYSQL_DB'))
            cls.cur = cls.conn.cursor()

    @classmethod
    def tearDownClass(cls) -> None:
        """Defines teardown for TestDBStorage"""
        if cls.conn and cls.cur:
            cls.cur.close()
            cls.conn.close()

    def setUp(self) -> None:
        """Defines setup for an instance method of TestDBStorage"""
        id_store = {}
        self.obj_insts = []
        for key, vals in classes_test.items():
            values = {}
            cls = classes[key]
            save_id = None
            for key, val in vals.items():
                if val == "save":
                    save_id = key
                elif not val:
                    values[key] = id_store[key]
                else:
                    values[key] = val
            obj_inst = cls(**values)
            obj_inst.save()
            self.obj_insts.append(obj_inst)
            if save_id:
                id_store[save_id] = obj_inst.id

    def tearDown(self) -> None:
        """Defines teardown for a instance method of TestDBStorage"""
        if self.obj_insts:
            for obj in self.obj_insts:
                models.storage.delete(obj)
        models.storage.save()
        models.storage.close()

    @ unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(models.storage.all()), dict)
        for cls in classes.values():
            self.assertIs(type(models.storage.all(cls)), dict)

    @ unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""
        all_objs = models.storage.all()
        self.assertEqual(len(all_objs), len(classes))

    @ unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """test that new adds an object to the database"""
        amenity_obj = Amenity(name="electricity")
        models.storage.new(amenity_obj)
        self.assertIn(amenity_obj, models.storage.all().values())
        models.storage.delete(amenity_obj)

    @ unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to dbStorage"""
        amenity_obj = Amenity(name="fan")
        models.storage.new(amenity_obj)
        models.storage.save()
        if self.cur:
            self.cur.execute(
                "SELECT name FROM `amenities` WHERE name = %s;",
                (amenity_obj.name, ))
            self.assertEqual(self.cur.fetchone()[0], amenity_obj.name)
        models.storage.delete(amenity_obj)
        models.storage.save()

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get(self):
        """Test the get method of the dbstorage"""
        first_state_id = list(models.storage.all(State).values())[0].id
        obj = models.storage.get(State, first_state_id)
        if obj:
            self.assertEqual(first_state_id, obj.id)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count(self):
        """Test count db method"""
        self.assertEqual(models.storage.count(State), 1)
        self.assertEqual(models.storage.count(), len(classes))
