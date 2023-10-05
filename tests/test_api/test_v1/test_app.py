#!/usr/bin/python3
"""Proceeds to import Flask and run host plus port"""


import os
from api.v1.app import app
from api.v1.views import *
import unittest
import tempfile
import flask

class TestApp(unittest.TestCase):
    """Test the app"""
    def create_app(self):
        """Test if the app is created"""
        with app.test_client() as client:
            self.assertIsInstance(client, flask.testing.FlaskClient)


if __name__ == "__main__":
    unittest.main()
