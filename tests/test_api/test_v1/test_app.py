#!/usr/bin/python3

"""Test api v1"""

import pep8
import unittest
from api.v1 import app
from api.v1.app import app as test_app


class TestApiDoc(unittest.TestCase):
    """Tests to check the documentation and style of app"""

    def test_pep8_conformance_app(self):
        """Test that api/v1/app.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['api/v1/app.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_app(self):
        """Test tests/test_api/test_v1/app.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(
            ['tests/test_api/test_v1/test_app.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_app_module_docstring(self):
        """Test for the app.py module docstring"""
        self.assertIsNot(app.__doc__, None,
                         "app.py needs a docstring")
        self.assertTrue(len(app.__doc__) >= 1,
                        "app.py needs a docstring")


class TestApiRoute(unittest.TestCase):
    """Test api routes """

    def setUp(self):
        """Setup app for testing"""
        test_app.testing = True
        self.app = test_app.test_client()

    def test_status(self):
        """Defines teardown class"""
        res = self.app.get('/api/v1/status')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json, {"status": "OK"})
