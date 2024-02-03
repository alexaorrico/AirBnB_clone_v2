#!/usr/bin/python3
"""
Test model Contains the TestDBStorageDocs, TestDBStorage, and TestFileStorage classes
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
result = pep8s.check_files(['tests/test_models/test_engine/test_db_storage.py'])
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
"""Test that all returns a dictionary"""
self.assertIs(type(models.storage.all()), dict)

@unittest.skipIf(models.storage_t != 'db', "not testing db storage")
def test_all_no_class(self):
"""Test that all returns all rows when no class is passed"""
storage = models.storage

# Add test objects to the storage for different classes
obj1 = Amenity()
obj2 = City()
# Add more objects for other classes if needed

# Save the objects to the storage
storage.new(obj1)
storage.new(obj2)
# Save more objects for other classes if needed

# Get all objects from the storage without specifying a class
all_objects = storage.all()

# Assert that the number of objects in the storage matches the expected count
self.assertEqual(len(all_objects), 2)
# Assert that the objects added are in the storage
self.assertIn(obj1, all_objects.values())
self.assertIn(obj2, all_objects.values())
# Assert for other classes if needed

@unittest.skipIf(models.storage_t != 'db', "not testing db storage")
def test_new(self):
"""Test that new adds an object to the database"""
storage = models.storage
obj = Amenity()

# Add the object to the storage
storage.new(obj)
# Save the changes to the storage
storage.save()

# Get the object from the storage using its ID
retrieved_obj = storage.get(Amenity, obj.id)

# Assert that the retrieved object is the same as the original object
self.assertEqual(retrieved_obj, obj)

@unittest.skipIf(models.storage_t != 'db', "not testing db storage")
def test_save(self):
"""Test that saveproperly saves objects to the db"""
storage = models.storage
obj = Amenity()

# Add the object to the storage
storage.new(obj)
# Save the changes to the storage
storage.save()

# Get the object from the storage using its ID
retrieved_obj = storage.get(Amenity, obj.id)

# Modify a property of the retrieved object
retrieved_obj.name = "Updated Amenity"

# Save the changes to the storage
storage.save()

# Get the object again from the storage using its ID
updated_obj = storage.get(Amenity, obj.id)

# Assert that the retrieved object is the same as the updated object
self.assertEqual(updated_obj, retrieved_obj)

@unittest.skipIf(models.storage_t != 'db', "not testing db storage")
def test_get(self):
"""Test that get retrieves an item in db properly"""
storage = models.storage
obj = Amenity()

# Add the object to the storage
storage.new(obj)
# Save the changes to the storage
storage.save()

# Get the object from the storage using its ID
retrieved_obj = storage.get(Amenity, obj.id)

# Assert that the retrieved object is the same as the original object
self.assertEqual(retrieved_obj, obj)

@unittest.skipIf(models.storage_t != 'db', "not testing db storage")
def test_count(self):
"""Test that count returns the right number of elements in the db"""
storage = models.storage

# Add test objects to the storage for different classes
obj1 = Amenity()
obj2 = City()
# Add more objects for other classes if needed

# Add the objects to the storage
storage.new(obj1)
storage.new(obj2)
# Add more objects for other classes if needed

# Save the changes to the storage
storage.save()

# Get the count of objects in the storage for each class
count1 = storage.count(Amenity)
count2 = storage.count(City)
# Get counts for other classes if needed

# Assert that the counts match the expected values
self.assertEqual(count1, 1)
self.assertEqual(count2, 1)
# Assert for other classes if needed


if __name__ == "__main__":
unittest.main()

