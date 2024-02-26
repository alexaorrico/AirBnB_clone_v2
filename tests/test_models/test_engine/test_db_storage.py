#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

import unittest
from datetime import datetime
import inspect
from models.engine.db_storage import DBStorage
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

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestDBStorage(unittest.TestCase):
    """Test the DBStorage class"""

    def setUp(self):
        """Set up the tests"""
        self.storage = DBStorage()
        self.storage.reload()
        self.new_user = User(email="test@example.com", password="testpass")

    def tearDown(self):
        """Clean up after each test"""
        if os.path.exists("file.json"):
            os.remove("file.json")

    def test_all_returns_dict(self):
        """Test that all returns a dictionary"""
        all_objs = self.storage.all()
        self.assertIsInstance(all_objs, dict)

    def test_all_with_class(self):
        """Test that all with class parameter returns correct objects"""
        self.storage.new(self.new_user)
        self.storage.save()
        all_users = self.storage.all(User)
        self.assertIn('User.' + self.new_user.id, all_users)

    def test_all_with_invalid_class(self):
        """Test that all with invalid class parameter returns an empty dict"""
        all_invalid = self.storage.all("InvalidClass")
        self.assertEqual(len(all_invalid), 0)

    def test_new(self):
        """Test that new adds an object to the database"""
        self.storage.new(self.new_user)
        key = 'User.' + self.new_user.id
        self.assertIn(key, self.storage.all())

    def test_save(self):
        """Test that save properly saves objects to the database"""
        self.storage.new(self.new_user)
        self.storage.save()
        with open("file.json", "r") as f:
            data = f.read()
            self.assertIn('User.' + self.new_user.id, data)

    def test_reload(self):
        """Test that reload properly loads objects from the database"""
        self.storage.new(self.new_user)
        self.storage.save()
        key = 'User.' + self.new_user.id
        self.storage.reload()
        reloaded_objs = self.storage.all()
        self.assertIn(key, reloaded_objs)

    def test_delete(self):
        """Test that delete removes an object from the database"""
        self.storage.new(self.new_user)
        key = 'User.' + self.new_user.id
        self.assertIn(key, self.storage.all())
        self.storage.delete(self.new_user)
        self.assertNotIn(key, self.storage.all())

    def test_delete_with_invalid_object(self):
        """Test that delete with an invalid object does nothing"""
        invalid_user = User()
        self.storage.delete(invalid_user)

    def test_close(self):
        """Test that close properly closes the session"""
        self.storage.close()

    def test_new_with_existing_object(self):
        """Test that new does not add an existing object to the database"""
        self.storage.new(self.new_user)
        self.storage.save()
        initial_count = len(self.storage.all(User))
        self.storage.new(self.new_user)
        self.storage.save()
        updated_count = len(self.storage.all(User))
        self.assertEqual(initial_count, updated_count)

    def test_all_with_multiple_classes(self):
        """Test that all with multiple classes returns correct objects"""
        user = User()
        city = City()
        amenity = Amenity()
        self.storage.new(user)
        self.storage.new(city)
        self.storage.new(amenity)
        self.storage.save()
        all_objs = self.storage.all([User, City, Amenity])
        self.assertIn('User.' + user.id, all_objs)
        self.assertIn('City.' + city.id, all_objs)
        self.assertIn('Amenity.' + amenity.id, all_objs)

    def test_save_with_multiple_objects(self):
        """Test that save properly saves multiple objects to the database"""
        user1 = User()
        user2 = User()
        city = City()
        self.storage.new(user1)
        self.storage.new(user2)
        self.storage.new(city)
        self.storage.save()
        with open("file.json", "r") as f:
            data = f.read()
            self.assertIn('User.' + user1.id, data)
            self.assertIn('User.' + user2.id, data)
            self.assertIn('City.' + city.id, data)

    def test_delete_with_invalid_id(self):
        """Test that delete with an invalid ID does nothing"""
        self.storage.new(self.new_user)
        self.storage.save()
        initial_count = len(self.storage.all(User))
        invalid_id = "invalid_id"
        invalid_user = User(id=invalid_id)
        self.storage.delete(invalid_user)
        updated_count = len(self.storage.all(User))
        self.assertEqual(initial_count, updated_count)

    def test_reload_with_invalid_data(self):
        """Test that reload with invalid data does not raise an error"""
        with open("file.json", "w") as f:
            f.write("Invalid JSON data")
        self.storage.reload()
    def test_close_with_no_session(self):
        """Test that close with no session does not raise an error"""
        self.storage.close()
    def test_close_with_open_session(self):
        """Test that close with an open session does not raise an error"""
        self.storage.reload()
        self.storage.close()

    def test_all_after_delete(self):
        """Test that all returns correct objects after deleting an object"""
        self.storage.new(self.new_user)
        self.storage.save()
        key = 'User.' + self.new_user.id
        self.assertIn(key, self.storage.all())
        self.storage.delete(self.new_user)
        self.assertNotIn(key, self.storage.all())

    def test_all_after_reload(self):
        """Test that all returns correct objects after reloading the storage"""
        self.storage.new(self.new_user)
        self.storage.save()
        key = 'User.' + self.new_user.id
        self.storage.reload()
        self.assertIn(key, self.storage.all())

    def test_new_with_invalid_object(self):
        """Test that new with an invalid object does nothing"""
        invalid_obj = "InvalidObject"
        self.storage.new(invalid_obj)
    def test_save_with_invalid_data(self):
        """Test that save with invalid data does not raise an error"""
        invalid_data = "Invalid JSON data"
        self.storage._DBStorage__objects = invalid_data
        self.storage.save()

if __name__ == "__main__":
    unittest.main()
