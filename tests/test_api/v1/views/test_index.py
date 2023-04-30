#!/usr/bin/python3
"""
Test cases for api redirections
"""

import inspect
"""import pep8"""
import unittest
from flask import Flask
from api.v1.app import app


class TestCityDocs(unittest.TestCase):
    """Tests to check the documentation and style of City class"""
    @classmethod
    def setUpClass(self):
        """Set up for the doc tests"""
        self.myapp = app.app_context()
        self.myapp.push()
        app.testing = True
        self.client = app.test_client()

    def test_status_code(self):
        """ Test for status """
        res = self.client.get('api/v1/status')
        self.assertEqual(res.status_code, 200)

    def test_content-type(self):
        """ Test return data """
        res = self.client.get('api/v1/status')
        self.assertEqual(res.content_type, 'application/json')
