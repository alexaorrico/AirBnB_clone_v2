#!/usr/bin/python3
"""
    Contains the class TestConsoleDocs
"""
import inspect
import pep8
import unittest
import requests
import json
from api.v1.views import index


class TestindexDocs(unittest.TestCase):
    """Class for testing documentation of the console"""
    def test_pep8_conformance_index(self):
        """Test that console.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['api/v1/views/index.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_index(self):
        """Test that tests/test_console.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_api/test_v1/test_views/test_index.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_index_module_docstring(self):
        """Test for the console.py module docstring"""
        self.assertIsNot(index.__doc__, None,
                         "app.py needs a docstring")
        self.assertTrue(len(index.__doc__) >= 1,
                        "app.py needs a docstring")

    def test_index_status_docstring(self):
        """Test for the HBNBCommand class docstring"""
        self.assertIsNot(index.status.__doc__, None,
                         "HBNBCommand class needs a docstring")
        self.assertTrue(len(index.status.__doc__) >= 1,
                        "HBNBCommand class needs a docstring")

    def test_index_stats_docstring(self):
        """Test for the HBNBCommand class docstring"""
        self.assertIsNot(index.stats.__doc__, None,
                         "HBNBCommand class needs a docstring")
        self.assertTrue(len(index.stats.__doc__) >= 1,
                        "HBNBCommand class needs a docstring")


class TestIndex(unittest.TestCase):
    """ test some apps up in this """

    @unittest.skip
    def test_error_page(self):
        """ test that error page up in this """
        req = requests.get('http://0.0.0.0:5000/api/v1/nop')
        self.assertDictEqual({"error": "Not found"},
                             json.loads(req.text))
        self.assertEqual(req.status_code, 404)

    def test_status(self):
        """ testdslaflsdkf asdf"""
        with app.app.test_client() as c:
            rv = c.post('/api/v1/status', json={'error': 'Not found'})
            json_data = rv.get_json()
            assert {"satus": "OK"} == json_data

    def test_stats(self):
        """ testdslaflsdkf asdf"""
        with app.app.test_client() as c:
            rv = c.post('/api/v1/stats', json={'error': 'Not found'})
            json_data = rv.get_json()
            list_of_classes = ['users', 'places', 'reviews', 'amenities', 'states', 'cities']
            json_list = json_data.keys()
            assert list_of_classes == json_list
