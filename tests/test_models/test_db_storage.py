#!/usr/bin/python3
"""Test BaseModel for expected behavior and documentation"""

from datetime import datetime
import inspect
import models
import pep8 as pycodestyle
import time
import unittest
from unittest import mock
BaseModel = models.base_model.BaseModel
module_doc = models.base_model.__doc__


class TestBaseModelDocs(unittest.TestCase):
    """Tests to check the documentation and style of BaseModel class"""
    def test_get_object(self):
        """Create an object and add it to the storage"""
        obj = SomeClass()
        obj_id = "unique_id"
        self.storage.save(obj)

        """Retrieve the object using the get method"""
        retrieved_obj = self.storage.get(SomeClass, obj_id)

        """Assert that the retrieved object matches the original one"""
        self.assertEqual(retrieved_obj, obj)

    def test_count_objects(self):
        """Create and add multiple objects to the storage"""
        obj1 = SomeClass()
        obj2 = SomeClass()
        obj3 = AnotherClass()
        self.storage.save(obj1)
        self.storage.save(obj2)
        self.storage.save(obj3)

        """Count the number of objects of SomeClass"""
        count = self.storage.count(SomeClass)
        self.assertEqual(count, 2)

        """Count the number of objects of AnotherClass"""
        count = self.storage.count(AnotherClass)
        self.assertEqual(count, 1)

        """Count the total number of objects"""
        count = self.storage.count()
        self.assertEqual(count, 3)
