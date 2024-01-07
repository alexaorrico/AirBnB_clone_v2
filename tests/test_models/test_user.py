#!/usr/bin/python3
"""
Unit Test for User Class
"""
from datetime import datetime
import inspect
import json
import models
from os import environ, stat
import pep8
import unittest

User = models.user.User
BaseModel = models.base_model.BaseModel
STORAGE_TYPE = environ.get('HBNB_TYPE_STORAGE')


class TestUserDocs(unittest.TestCase):
    """Class for testing User Class docs"""

    all_funcs = inspect.getmembers(User, inspect.isfunction)

    @classmethod
    def setUpClass(cls):
        print('\n\n.................................')
        print('..... Testing Documentation .....')
        print('........   User  Class   ........')
        print('.................................\n\n')

    def test_doc_file(self):
        """... documentation for the file"""
        expected = '\nUser Class from Models Module\n'
        actual = models.user.__doc__
        self.assertEqual(expected, actual)

    def test_doc_class(self):
        """... documentation for the class"""
        actual = User.__doc__
        self.assertIsNotNone(actual)

    def test_all_function_docs(self):
        """... tests for ALL DOCS for all functions in db_storage file"""
        all_functions = TestUserDocs.all_funcs
        for function in all_functions:
            self.assertIsNotNone(function[1].__doc__)

    def test_pep8_user(self):
        """... user.py conforms to PEP8 Style"""
        pep8style = pep8.StyleGuide(quiet=True)
        errors = pep8style.check_files(['models/user.py'])
        self.assertEqual(errors.total_errors, 0, errors.messages)

    def test_file_is_executable(self):
        """... tests if file has correct permissions so user can execute"""
        file_stat = stat('models/user.py')
        permissions = str(oct(file_stat[0]))
        actual = int(permissions[5:-2]) >= 5
        self.assertTrue(actual)


class TestUserInstances(unittest.TestCase):
    """testing for class instances"""

    @classmethod
    def setUpClass(cls):
        print('\n\n.................................')
        print('....... Testing Functions .......')
        print('.........  User  Class  .........')
        print('.................................\n\n')

    def setUp(self):
        """initializes new user for testing"""
        self.user = User()

    def test_instantiation(self):
        """... checks if User is properly instantiated"""
        self.assertIsInstance(self.user, User)

    @unittest.skipIf(STORAGE_TYPE == 'db', 'skip if environ is db')
    def test_to_string(self):
        """... checks if BaseModel is properly casted to string"""
        my_str = str(self.user)
        my_list = ['User', 'id', 'created_at']
        actual = 0
        for sub_str in my_list:
            if sub_str in my_str:
                actual += 1
        self.assertTrue(3 == actual)

    @unittest.skipIf(STORAGE_TYPE == 'db', 'skip if environ is db')
    def test_instantiation_no_updated(self):
        """... should not have updated attribute"""
        self.user = User()
        my_str = str(self.user)
        actual = 0
        if 'updated_at' in my_str:
            actual += 1
        self.assertTrue(0 == actual)

    @unittest.skipIf(STORAGE_TYPE == 'db', 'skip if environ is db')
    def test_updated_at(self):
        """... save function should add updated_at attribute"""
        self.user.save()
        actual = type(self.user.updated_at)
        expected = type(datetime.now())
        self.assertEqual(expected, actual)

    @unittest.skipIf(STORAGE_TYPE == 'db', 'skip if environ is db')
    def test_to_json(self):
        """... to_json should return serializable dict object"""
        self.user_json = self.user.to_json()
        actual = 1
        try:
            serialized = json.dumps(self.user_json)
        except:
            actual = 0
        self.assertTrue(1 == actual)

    @unittest.skipIf(STORAGE_TYPE == 'db', 'skip if environ is db')
    def test_json_class(self):
        """... to_json should include class key with value User"""
        self.user_json = self.user.to_json()
        actual = None
        if self.user_json['__class__']:
            actual = self.user_json['__class__']
        expected = 'User'
        self.assertEqual(expected, actual)

    def test_email_attribute(self):
        """... add email attribute"""
        self.user.email = "bettyholbertn@gmail.com"
        if hasattr(self.user, 'email'):
            actual = self.user.email
        else:
            actual = ''
        expected = "bettyholbertn@gmail.com"
        self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main
