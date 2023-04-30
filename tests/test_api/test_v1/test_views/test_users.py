#!/usr/bin/python3
"""
Contains tests for views place reviews routes
"""

import unittest

from api.v1.app import app
from models import storage
from models.user import User


class TestViewsPlaceReviews(unittest.TestCase):
    """Test Class for Views Place Reviews routes
    """

    def setUp(self):
        """Sets up the flask app for testing"""
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()
        self.user_1 = User(email="abebe@example.com", password="12345")
        self.user_2 = User(email="alemitu@example.com", password="12345")
        storage.new(self.user_1)
        storage.new(self.user_2)
        storage.save()

    def tearDown(self):
        """Removes the flask app context"""
        storage.delete(self.user_1)
        storage.delete(self.user_2)
        storage.save()
        self.ctx.pop()

    def test_users_endpoint(self):
        """Tests the /users endpoint returns list of users
        """
        response = self.client.get("/api/v1/users")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        data = list(response.get_json())
        result = filter(
            lambda user: user["id"] == self.user_1.id,
            data,
        )
        self.assertIsNotNone(next(result))
