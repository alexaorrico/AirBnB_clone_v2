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
import subprocess
import pep8
import unittest
DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}

# initialize new instance of hbnb_test_db
if models.storage_t == 'db':
    # cmd line: HBNB_ENV=test HBNB_MYSQL_USER=hbnb_test \
    #           HBNB_MYSQL_PWD=hbnb_test_pwd \
    #           HBNB_MYSQL_HOST=localhost \
    #           HBNB_MYSQL_DB=hbnb_test_db \
    #           HBNB_TYPE_STORAGE=db \
    #           python3 -m unittest discover tests
    storage = DBStorage()
    # populate empty hbnb_test_db with 7-dump.sql
    # !!! must have hbnb_test user created !!!
    #    and with permission to hbnb_test_db
    #     run setup_mysql_test.sql as root
    subprocess.call("./populate_test_db.sh", shell=True)
    storage.reload()


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
    """Test the FileStorage class"""
    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionary"""
        states_dict = storage.all("State")
        self.assertIs(type(states_dict), dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""
        state_names = [
            'Alabama', 'Arizona', 'California',
            'Colorado', 'Florida', 'Georgia',
            'Hawaii', 'Illinois', 'Indiana',
            'Louisiana', 'Minnesota',
            'Mississippi', 'Oregon'
        ]
        city_names = [
            'Joliet', 'Tupelo', 'Babbie', 'Kearny',
            'Tempe', 'Calera', 'Miami', 'Jackson',
            'Saint Paul', 'Baton rouge', 'Sonoma',
            'Lafayette', 'Peoria', 'Fremont', 'Denver',
            'Chicago', 'Honolulu', 'Orlando', 'Douglas',
            'Portland', 'Akron', 'Eugene', 'New Orleans',
            'San Jose', 'Meridian', 'Urbana', 'Kailua',
            'Napa', 'Naperville', 'Pearl city',
            'Fairfield', 'San Francisco'
        ]
        # known inital import data
        initial_data = state_names + city_names

        # load object from db_storage
        items = storage.all().values()

        all_items = []
        for item in items:
            all_items.append(item.name)

        # are they different
        not_in_initial = list(set(initial_data)-set(all_items))
        not_in_all_items = list(set(all_items)-set(initial_data))
        # list of combined differences
        diff = list(not_in_initial + not_in_all_items)
        self.assertTrue(diff == [])

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """test that new adds an object to the database"""
        # add objects to the session using State
        states = storage.all("State").values()

        # create list of states as base case
        before = []
        for state in states:
            before.append(state.name)
        # create new State object
        new_state = State(name="Fake_State")

        # call new function ; update objects of the session
        storage.new(new_state)
        states = storage.all("State").values()

        # create test list of states
        after = []
        for state in states:
            after.append(state.name)

        # only one item was added
        self.assertTrue(len(after) - len(before) == 1)

        # the item added was 'Fake_State'
        not_in_before = list(set(before)-set(after))
        not_in_after = list(set(after)-set(before))
        diff = list(not_in_before + not_in_after)
        self.assertTrue(diff[0] == "Fake_State")

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_delete(self):
        """Test that save properly saves objects to file.json"""
        # add objects to the session using State
        new_state = State(name="Fake_State")
        storage.new(new_state)
        storage.save()
        states = storage.all("State").values()

        # create list of states as base case
        before = []
        for state in states:
            before.append(state.name)
        # create new State object

        # call new function ; update objects of the session
        storage.delete(new_state)
        storage.save()
        states = storage.all("State").values()

        # create test list of states
        after = []
        for state in states:
            after.append(state.name)

        # only one item was deleted
        self.assertTrue(len(after) - len(before) == -1)

        # the item deleted was 'Fake_State'
        not_in_before = list(set(before)-set(after))
        not_in_after = list(set(after)-set(before))
        diff = list(not_in_before + not_in_after)
        self.assertTrue(diff[0] == "Fake_State")

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """
        Save is called in test_new and in test_delete.
        If the storage items, mysql data objects, are not persisted, meaing
        saved/commited to the database, then an error occurs:
                Instance '<State at 0x7fc0980ffdd8>' is not persisted.
        Therefore, save is verified working during the delete test
        """
        pass

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_dbcount(self):
        """tests count"""
        pre = storage.count("Amenity")
        test_obj = Amenity(name="foo")
        storage.new(test_obj)
        post = storage.count("Amenity")
        self.assertEqual(pre + 1, post)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_dbget(self):
        """tests get"""
        test_obj = Amenity(name="bar")
        storage.new(test_obj)
        data = storage.get("Amenity", test_obj.id)
        self.assertEqual(id(test_obj), id(data))
