#!/usr/bin/python3
"""
tests for api states
"""

import inspect
import ṕep8
import web_flask
import unitttest
from os import stat
import api
file = api.v1.views.states


class TestDocStates(unittest.TestCase):
    """ testing doctrings"""

    functions = inspect.getmembers(module, inspect.isfunction)

    @classmethod
    def setUpClass(cls):
        print('\n\n.................................')
        print('..... Testing Documentation .....')
        print('.......  States API  .......')
        print('.................................\n\n')

    def test_file_documentation(self):
        """ checking docstrings """
        doc_string = module.__doc__
        self.assertIsNotNone(doc_string)

    def test_pep8_complain(self):
        """ verify zero pep8 errors """
        pep8_ok = pep8.StyleGuide(quiet=True)
        erros = pep8_ok.check_files(['api/v1/views/states.py'])
        self.assertEqual(errors.total_errors, 0, errors.messages)


if __name__ == "__main__":
    """ if main tests """
    unittest.main
