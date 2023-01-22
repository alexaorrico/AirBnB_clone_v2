#!/usr/bin/python3
"""
Contains tests for views index blueprint
"""

import unittest

from api.v1.app import app


class TestViewsIndex(unittest.TestCase):
    """Test Class for Views Index Blueprint
    """

    def setUp(self):
        """Sets up the flask app for testing"""
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()

    def tearDown(self):
        """Removes the flask app context"""
        self.ctx.pop()

    def test_app_status(self):
        """Test wether the status route returns 200"""
        response = self.client.get("/api/v1/status")
        self.assertEqual(response.status_code, 200)

    def test_app_json(self):
        """Test wether the status route returns 200"""
        response = self.client.get("/api/v1/status")
        self.assertEqual(response.content_type, "application/json")
        self.assertIsNotNone(response.json["status"])

    def test_app_stats(self):
        """Test stats route returns a json with 200 status code"""
        response = self.client.get("/api/v1/stats")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")

    def test_app_stats_returns_full_data(self):
        """Test stats route returns a json with all the tables as keys"""
        response = self.client.get("/api/v1/stats")
        data = response.get_json()
        self.assertIn("amenities", data)
        self.assertIn("cities", data)
        self.assertIn("places", data)
        self.assertIn("reviews", data)
        self.assertIn("states", data)
        self.assertIn("users", data)

    def test_app_stats_returns_valid_number(self):
        """Test stats route returns a json with valid int counts"""
        response = self.client.get("/api/v1/stats")
        data = response.get_json()
        self.assertTrue(isinstance(data.get("amenities", None), int))
        self.assertTrue(isinstance(data.get("cities", None), int))
        self.assertTrue(isinstance(data.get("places", None), int))
        self.assertTrue(isinstance(data.get("reviews", None), int))
        self.assertTrue(isinstance(data.get("states", None), int))
        self.assertTrue(isinstance(data.get("users", None), int))
