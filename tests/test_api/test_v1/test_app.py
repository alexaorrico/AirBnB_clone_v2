#!/usr/bin/python3
"""
Unit Test for api v1 Flask App
"""
from api.v1 import app
import inspect
import pep8
import unittest


class TestAppDocs(unittest.TestCase):
    """Class for testing Flask App docs"""

    all_funcs = inspect.getmembers(app, inspect.isfunction)

    @classmethod
    def setUpClass(cls):
        print('\n\n.................................')
        print('..... Testing Documentation .....')
        print('........  For Flask App  ........')
        print('.................................\n\n')

    def test_doc_file(self):
        """... documentation for the file"""
        actual = app.__doc__
        self.assertIsNotNone(actual)

    def test_all_function_docs(self):
        """... tests for ALL DOCS for all functions in db_storage file"""
        all_functions = TestAppDocs.all_funcs
        for function in all_functions:
            self.assertIsNotNone(function[1].__doc__)

    def test_pep8_app(self):
        """... app.py conforms to PEP8 Style"""
        pep8style = pep8.StyleGuide(quiet=True)
        errors = pep8style.check_files(['api/v1/app.py'])
        self.assertEqual(errors.total_errors, 0, errors.messages)


if __name__ == '__main__':
    """
    MAIN TESTS
    """
    unittest.main
