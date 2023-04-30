#!/usr/bin/python3
"""
Contains the TestCityDocs classes
"""

import inspect
import unittest
from flask import Flask
from api.v1.app import app

class TestFlaskApp(unittest.TestCase):
    """Tests to check the documentation and style of City class"""
    @classmethod
    def setUpClass(self):
        """init flask app"""
        self.myapp = app.app_context()
        self.myapp.push()
        self.client = app.test_client()

    def test_404_Not_found(self):
        """Test 404 error handler"""
        res = self.client.get('api/v1/nil')
        self.assertEqual(res.status_code, 404)
