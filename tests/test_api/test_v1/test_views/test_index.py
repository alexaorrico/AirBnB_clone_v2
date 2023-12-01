#!/usr/bin/python3
"""
Contains TestIndexApiDocs and TestIndexApi classes
"""

import unittest
import requests
import pep8
from api.v1.views import index

apis = ["amenities", "cities", "places",
        "reviews", "states", "users"]


class TestIndexApiDocs(unittest.TestCase):
    """Tests to check the documentation and style of Index Api module"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""

    def test_pep8_conformance_index(self):
        """Test that api/v1/views/index.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['api/v1/views/index.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_index(self):
        """Test that tests/test_api/test_v1/test_views/test_index.py
        conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(
                ['tests/test_api/test_v1/test_views/test_index.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_index_module_docstring(self):
        """Test for the index.py module docstring"""
        self.assertIsNot(index.__doc__, None,
                         "ameniies.py needs a docstring")
        self.assertTrue(len(index.__doc__) >= 1,
                        "index.py needs a docstring")

    """
    def test_index_func_docstrings(self):
        Test for the presence of docstrings in Index methods
        for func in self.index_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))
     """


class TestAmeniteisApi(unittest.TestCase):
    """Tests to check the Index api module"""
    api_url = "http://127.0.0.1:5000/api/v1/"

    def test_index_GET_status_route(self):
        """Test the GET status route in index """
        status_route = "{}/status".format(self.api_url)
        r = requests.get(status_route)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.headers['content-type'], 'application/json')
        self.assertEqual(len(r.json()), 1)
        self.assertTrue("status" in r.json())

    def test_index_GET_stats_route(self):
        """Test the GET stats route in index """
        stats_route = "{}/stats".format(self.api_url)
        r = requests.get(stats_route)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.headers['content-type'], 'application/json')
        self.assertEqual(len(r.json()), len(apis))
        for value in apis:
            self.assertTrue(value in r.json())
