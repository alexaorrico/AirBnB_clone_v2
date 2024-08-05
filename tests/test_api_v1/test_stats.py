#!/usr/bin/python3
"""Test API stats endpoint"""

import unittest
from flask import json
from api.v1.app import app

class TestStatsAPI(unittest.TestCase):
    """Tests for the /api/v1/stats endpoint"""

    @classmethod
    def setUpClass(cls):
        """Set up the test client"""
        cls.client = app.test_client()

    def test_stats(self):
        """Test the /api/v1/stats endpoint"""
        response = self.client.get('/api/v1/stats')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("amenities", data)
        self.assertIn("cities", data)
        self.assertIn("places", data)
        self.assertIn("reviews", data)
        self.assertIn("states", data)
        self.assertIn("users", data)
        self.assertIsInstance(data["amenities"], int)
        self.assertIsInstance(data["cities"], int)
        self.assertIsInstance(data["places"], int)
        self.assertIsInstance(data["reviews"], int)
        self.assertIsInstance(data["states"], int)
        self.assertIsInstance(data["users"], int)

if __name__ == '__main__':
    unittest.main()
