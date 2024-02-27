#!/usr/bin/python3
"""
Unit Test for BaseModel Class
"""
from datetime import datetime
import inspect
import json
import models
from os import environ, stat
import pep8
import unittest

BaseModel = models.base_model.BaseModel
STORAGE_TYPE = environ.get('HBNB_TYPE_STORAGE')


class TestBaseModelDocs(unittest.TestCase):
    """Class for testing BaseModel docs"""

    all_funcs = inspect.getmembers(BaseModel, inspect.isfunction)

    @classmethod
    def setUpClass(cls):
        print('\n\n.................................')
        print('..... Testing Documentation .....')
        print('.....  For BaseModel Class  .....')
        print('.................................\n\n')

    def test_doc_file(self):
        """... documentation for the file"""
        expected = '\nBaseModel Class of Models Module\n'
        actual = models.base_model.__doc__
        self.assertEqual(expected, actual)

    def test_doc_class(self):
        """... documentation for the class"""
        expected = ('\n        attributes and functions for BaseModel class\n'
                    '    ')
        actual = BaseModel.__doc__
        self.assertEqual(expected, actual)

    def test_all_function_docs(self):
        """... tests for ALL DOCS for all functions in db_storage file"""
        all_functions = TestBaseModelDocs.all_funcs
        for function in all_functions:
            self.assertIsNotNone(function[1].__doc__)

    def test_pep8_base_model(self):
        """... base_model.py conforms to PEP8 Style"""
        pep8style = pep8.StyleGuide(quiet=True)
        errors = pep8style.check_files(['models/base_model.py'])
        self.assertEqual(errors.total_errors, 0, errors.messages)

    def test_file_is_executable(self):
        """... tests if file has correct permissions so user can execute"""
        file_stat = stat('models/base_model.py')
        permissions = str(oct(file_stat[0]))
        actual = int(permissions[5:-2]) >= 5
        self.assertTrue(actual)


@unittest.skipIf(STORAGE_TYPE == 'db', 'DB Storage does not store BaseModel')
class TestBaseModelInstances(unittest.TestCase):
    """testing for class instances"""

    @classmethod
    def setUpClass(cls):
        print('\n\n.................................')
        print('....... Testing Functions .......')
        print('.....  For BaseModel Class  .....')
        print('.................................\n\n')

    def setUp(self):
        """initializes new BaseModel instance for testing"""
        self.model = BaseModel()

    def test_instantiation(self):
        """... checks if BaseModel is properly instantiated"""
        self.assertIsInstance(self.model, BaseModel)

    def test_to_string(self):
        """... checks if BaseModel is properly casted to string"""
        my_str = str(self.model)
        my_list = ['BaseModel', 'id', 'created_at']
        actual = 0
        for sub_str in my_list:
            if sub_str in my_str:
                actual += 1
        self.assertTrue(3 == actual)

    def test_to_string(self):
        """... checks if BaseModel is properly casted to string"""
        my_str = str(self.model)
        my_list = ['BaseModel', 'id', 'created_at']
        actual = 0
        for sub_str in my_list:
            if sub_str in my_str:
                actual += 1
        self.assertTrue(3 == actual)

    def test_instantiation_no_updated(self):
        """... should not have updated attribute"""
        my_str = str(self.model)
        actual = 0
        if 'updated_at' in my_str:
            actual += 1
        self.assertTrue(0 == actual)

    def test_save(self):
        """... save function should add updated_at attribute"""
        self.model.save()
        actual = type(self.model.updated_at)
        expected = type(datetime.now())
        self.assertEqual(expected, actual)

    def test_to_json(self):
        """... to_json should return serializable dict object"""
        my_model_json = self.model.to_json()
        actual = 1
        try:
            serialized = json.dumps(my_model_json)
        except:
            actual = 0
        self.assertTrue(1 == actual)

    def test_json_class(self):
        """... to_json should include class key with value BaseModel"""
        my_model_json = self.model.to_json()
        actual = None
        if my_model_json['__class__']:
            actual = my_model_json['__class__']
        expected = 'BaseModel'
        self.assertEqual(expected, actual)

    def test_name_attribute(self):
        """... add name attribute"""
        self.model.name = "Holberton"
        actual = self.model.name
        expected = "Holberton"
        self.assertEqual(expected, actual)

    def test_number_attribute(self):
        """... add number attribute"""
        self.model.number = 98
        actual = self.model.number
        self.assertTrue(98 == actual)

if __name__ == '__main__':
    """
    MAIN TESTS
    """
    unittest.main
