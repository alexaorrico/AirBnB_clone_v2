#!/usr/bin/python3
"""
Unit Test for api v1 Flask App
"""
import inspect
import pep8
import web_flask
import unittest
from os import stat
import api
module = __import__('1-pack_web_static', globals(), locals(), ['*'])


class TestPackWebStaticDocs(unittest.TestCase):
    """Class for testing Hello Route docs"""

    all_funcs = inspect.getmembers(module, inspect.isfunction)

    @classmethod
    def setUpClass(cls):
        print('\n\n.................................')
        print('..... Testing Documentation .....')
        print('.......  PackWebStatic API  .......')
        print('.................................\n\n')

    def test_doc_file(self):
        """... documentation for the file"""
        actual = module.__doc__
        self.assertIsNotNone(actual)

    def test_all_function_docs(self):
        """... tests for ALL DOCS for all functions"""
        all_functions = TestPackWebStaticDocs.all_funcs
        for function in all_functions:
            self.assertIsNotNone(function[1].__doc__)

    def test_pep8(self):
        """... tests if file conforms to PEP8 Style"""
        pep8style = pep8.StyleGuide(quiet=True)
        errors = pep8style.check_files(['1-pack_web_static.py'])
        self.assertEqual(errors.total_errors, 0, errors.messages)

    def test_file_is_executable(self):
        """... tests if file has correct permissions so user can execute"""
        file_stat = stat('1-pack_web_static.py')
        permissions = str(oct(file_stat[0]))
        self.assertEqual(permissions[5:], "775")


if __name__ == '__main__':
    """
    MAIN TESTS
    """
    unittest.main
