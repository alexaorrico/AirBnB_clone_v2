# tests/test_state.py

import unittest
from flask import Flask
from api.v1.views import app_views
from models import storage, State

class TestStateRoute(unittest.TestCase):
    """Test cases for the State view."""

    def setUp(self):
        """Set up the test environment."""
        self.app = Flask(__name__)
        app_views.app.config["TESTING"] = True
        self.client = app_views.app.test_client()

    def tearDown(self):
        """Tear down the test environment."""
        pass 

    def test_get_states_route(self):
        """Test the /states route (GET)."""
        # Create and save some State objects for testing
        state1 = State(name="State 1")
        state2 = State(name="State 2")
        state1.save()
        state2.save()

        response = self.client.get("/api/v1/states")
        self.assertEqual(response.status_code, 200)
        # Check response JSON for expected keys and values
        self.assertIn("State 1", response.json)
        self.assertIn("State 2", response.json)

    

if __name__ == "__main__":
    unittest.main()
