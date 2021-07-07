#!/usr/bin/python3
"""
    Contains the class TestConsoleDocs
"""
import inspect
import pep8
import unittest
import requests
import json
from api.v1 import app


class TestappDocs(unittest.TestCase):
    """Class for testing documentation of the console"""
    def test_pep8_conformance_app(self):
        """Test that console.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['api/v1/app.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_app(self):
        """Test that tests/test_console.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_api/test_v1/test_app.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_app_module_docstring(self):
        """Test for the console.py module docstring"""
        self.assertIsNot(app.__doc__, None,
                         "app.py needs a docstring")
        self.assertTrue(len(app.__doc__) >= 1,
                        "app.py needs a docstring")

    def test_app_dudewermypge_docstring(self):
        """Test for the HBNBCommand class docstring"""
        self.assertIsNot(app.dudewermypge.__doc__, None,
                         "HBNBCommand class needs a docstring")
        self.assertTrue(len(app.dudewermypge.__doc__) >= 1,
                        "HBNBCommand class needs a docstring")

    def test_app_tearthatmotherfuckerdown_docstring(self):
        """Test for the HBNBCommand class docstring"""
        self.assertIsNot(app.tearthatmotherfuckerdown.__doc__, None,
                         "HBNBCommand class needs a docstring")
        self.assertTrue(len(app.tearthatmotherfuckerdown.__doc__) >= 1,
                        "HBNBCommand class needs a docstring")


class TestApp(unittest.TestCase):
    """ test some apps up in this """

    @unittest.skip
    def test_error_page(self):
        """ test that error page up in this """
        req = requests.get('http://0.0.0.0:5000/api/v1/nop')
        self.assertDictEqual({"error": "Not found"},
                             json.loads(req.text))
        self.assertEqual(req.status_code, 404)

    def test_err2(self):
        """ testdslaflsdkf asdf"""
        with app.app.test_client() as c:
            rv = c.post('/api/v1/nop', json={'error': 'Not found'})
            json_data = rv.get_json()
            assert {"error": "Not found"} == json_data
