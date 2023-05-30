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
DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}

def test_get_existing_object(self):
    # Create a test object in the storage
    obj = SomeClass(id='object_id', name='Test Object')
    self.storage.save(obj)

    # Retrieve the object using the get method
    retrieved_obj = self.storage.get(SomeClass, 'object_id')

    # Assert that the retrieved object matches the original object
    self.assertEqual(retrieved_obj, obj)

    def test_get_nonexistent_object(self):
        retrieved_obj = self.storage.get(SomeClass, 'nonexistent_id')

    # Assert that the retrieved object is None
    self.assertIsNone(retrieved_obj)

    def test_count_all_objects(self):
    # Create some test objects in the storage
        obj1 = SomeClass(id='object1', name='Object 1')
        obj2 = SomeClass(id='object2', name='Object 2')
        self.storage.save(obj1)
        self.storage.save(obj2)

    # Count all objects in the storage
    count = self.storage.count()

    # Assert that the count matches the number of objects created
    self.assertEqual(count, 2)

    def test_count_objects_by_class(self):
    # Create some test objects in the storage
       obj1 = SomeClass(id='object1', name='Object 1')
       obj2 = AnotherClass(id='object2', name='Object 2')
       self.storage.save(obj1)
       self.storage.save(obj2)

     # Count objects of SomeClass in the storage
    count = self.storage.count(SomeClass)

    # Assert that the count matches the number of objects of SomeClass
    self.assertEqual(count, 1)
