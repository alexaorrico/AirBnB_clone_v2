# tests/test_users.py

import unittest
from flask import Flask
from api.v1.views import app_views
from models import storage, User

class TestUsersRoute(unittest.TestCase):
    """Test cases for the Users view."""

    def setUp(self):
        """Set up the test environment."""
        self.app = Flask(__name__)
        app_views.app.config["TESTING"] = True
        self.client = app_views.app.test_client()

    def tearDown(self):
        """Tear down the test environment."""
        storage.close()

    def test_get_users_route(self):
        """Test the /users route (GET).
         Create and save some User objects for testing"""
        user1 = User(email="user1@example.com", password="password1")
        user2 = User(email="user2@example.com", password="password2")
        user1.save()
        user2.save()

        response = self.client.get("/api/v1/users")
        self.assertEqual(response.status_code, 200)
        # Check the response JSON for expected keys and values
        self.assertIn("user1@example.com", response.json)
        self.assertIn("user2@example.com", response.json)



if __name__ == "__main__":
    unittest.main()
