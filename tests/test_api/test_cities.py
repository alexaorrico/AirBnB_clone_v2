# tests/test_cities.py

import unittest
from flask import Flask
from api.v1.views import app_views
from models import storage, State, City

class TestCitiesRoute(unittest.TestCase):
    """Test cases for the Cities view."""

    def setUp(self):
        """Set up the test environment."""
        self.app = Flask(__name__)
        app_views.app.config["TESTING"] = True
        self.client = app_views.app.test_client()

    def tearDown(self):
        """Tear down the test environment."""
        storage.close()

    def test_get_cities_by_state_route(self):
        """Test the /states/<state_id>/cities route (GET)."""
        # Create and save a State object for testing
        state = State(name="Test State")
        state.save()

        # Create and save some City objects linked to the state
        city1 = City(name="City 1", state_id=state.id)
        city2 = City(name="City 2", state_id=state.id)
        city1.save()
        city2.save()

        response = self.client.get(f"/api/v1/states/{state.id}/cities")
        self.assertEqual(response.status_code, 200)
        # Check response JSON for expected keys and values
        self.assertIn("City 1", response.json)
        self.assertIn("City 2", response.json)



if __name__ == "__main__":
    unittest.main()
