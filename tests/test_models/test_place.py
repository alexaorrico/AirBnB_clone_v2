#!/usr/bin/python3
"""
Unit Test for Place Class
"""
from datetime import datetime
import inspect
import json
import models
from os import environ, stat
import pep8
import unittest

Place = models.place.Place
BaseModel = models.base_model.BaseModel
STORAGE_TYPE = environ.get('HBNB_TYPE_STORAGE')


class TestPlaceDocs(unittest.TestCase):
    """Class for testing BaseModel docs"""

    all_funcs = inspect.getmembers(Place, inspect.isfunction)

    @classmethod
    def setUpClass(cls):
        print('\n\n.................................')
        print('..... Testing Documentation .....')
        print('........   Place Class   ........')
        print('.................................\n\n')

    def test_doc_file(self):
        """... documentation for the file"""
        expected = '\nPlace Class from Models Module\n'
        actual = models.place.__doc__
        self.assertEqual(expected, actual)

    def test_doc_class(self):
        """... documentation for the class"""
        expected = 'Place class handles all application places'
        actual = Place.__doc__
        self.assertEqual(expected, actual)

    def test_all_function_docs(self):
        """... tests for ALL DOCS for all functions in db_storage file"""
        all_functions = TestPlaceDocs.all_funcs
        for function in all_functions:
            self.assertIsNotNone(function[1].__doc__)

    def test_pep8_place(self):
        """... place.py conforms to PEP8 Style"""
        pep8style = pep8.StyleGuide(quiet=True)
        errors = pep8style.check_files(['models/place.py'])
        self.assertEqual(errors.total_errors, 0, errors.messages)

    def test_file_is_executable(self):
        """... tests if file has correct permissions so user can execute"""
        file_stat = stat('models/place.py')
        permissions = str(oct(file_stat[0]))
        actual = int(permissions[5:-2]) >= 5
        self.assertTrue(actual)


class TestPlaceInstances(unittest.TestCase):
    """testing for class instances"""

    @classmethod
    def setUpClass(cls):
        print('\n\n.................................')
        print('....... Testing Functions .......')
        print('.........  Place Class  .........')
        print('.................................\n\n')

    def setUp(self):
        """initializes new place for testing"""
        self.place = Place()

    def test_instantiation(self):
        """... checks if Place is properly instantiated"""
        self.assertIsInstance(self.place, Place)

    @unittest.skipIf(STORAGE_TYPE == 'db', 'skip if environ is db')
    def test_to_string(self):
        """... checks if BaseModel is properly casted to string"""
        my_str = str(self.place)
        my_list = ['Place', 'id', 'created_at']
        actual = 0
        for sub_str in my_list:
            if sub_str in my_str:
                actual += 1
        self.assertTrue(3 == actual)

    @unittest.skipIf(STORAGE_TYPE == 'db', 'skip if environ is db')
    def test_instantiation_no_updated(self):
        """... should not have updated attribute"""
        my_str = str(self.place)
        actual = 0
        if 'updated_at' in my_str:
            actual += 1
        self.assertTrue(0 == actual)

    @unittest.skipIf(STORAGE_TYPE == 'db', 'skip if environ is db')
    def test_updated_at(self):
        """... save function should add updated_at attribute"""
        self.place.save()
        actual = type(self.place.updated_at)
        expected = type(datetime.now())
        self.assertEqual(expected, actual)

    @unittest.skipIf(STORAGE_TYPE == 'db', 'skip if environ is db')
    def test_to_json(self):
        """... to_json should return serializable dict object"""
        self.place_json = self.place.to_json()
        actual = 1
        try:
            serialized = json.dumps(self.place_json)
        except:
            actual = 0
        self.assertTrue(1 == actual)

    @unittest.skipIf(STORAGE_TYPE == 'db', 'skip if environ is db')
    def test_json_class(self):
        """... to_json should include class key with value Place"""
        self.place_json = self.place.to_json()
        actual = None
        if self.place_json['__class__']:
            actual = self.place_json['__class__']
        expected = 'Place'
        self.assertEqual(expected, actual)

    def test_guest_attribute(self):
        """... add guest attribute"""
        self.place.max_guest = 3
        if hasattr(self.place, 'max_guest'):
            actual = self.place.max_guest
        else:
            actual = ''
        expected = 3
        self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main
