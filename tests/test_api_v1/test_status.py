#!/usr/bin/python3
"""Unit tests for the /status endpoint"""

import unittest
from flask import jsonify
from api.v1.app import app

class TestStatusEndpoint(unittest.TestCase):
    """Test the /status endpoint"""

    @classmethod
    def setUpClass(cls):
        """Set up the Flask test client"""
        cls.client = app.test_client()
        cls.client.testing = True

    def test_status(self):
        """Test that the /status endpoint returns a 200 status code and JSON response"""
        response = self.client.get('/api/v1/status')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json, {"status": "OK"})

if __name__ == '__main__':
    unittest.main()
