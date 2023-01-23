#!/usr/bin/python3
"""
Contains tests for api v1 app
"""

import unittest

from api.v1.app import app


class TestApp(unittest.TestCase):
    """Test Class for Flask App
    """

    def setUp(self):
        """Sets up the flask app for testing"""
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()

    def tearDown(self):
        """Removes the flask app context"""
        self.ctx.pop()

    def test_app_404(self):
        """Test wether the 404 status is sent as json error message"""
        response = self.client.get("/api/v1/nop")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json["error"], "Not found")
