# tests/test_places.py

import unittest
from flask import Flask
from api.v1.views import app_views
from models import storage, Place, City, User

class TestPlacesRoute(unittest.TestCase):
    """Test cases for the Places view."""

    def setUp(self):
        """Set up the test environment."""
        self.app = Flask(__name__)
        app_views.app.config["TESTING"] = True
        self.client = app_views.app.test_client()

    def tearDown(self):
        """Tear down the test environment."""
        storage.close()

    def test_get_places_by_city_route(self):
        """Test the /cities/<city_id>/places route (GET).
         Create and save some City, User, and Place objects for testing"""
        city = City(name="Test City")
        user = User(email="user@example.com", password="password")
        place1 = Place(name="Place 1", city_id=city.id, user_id=user.id)
        place2 = Place(name="Place 2", city_id=city.id, user_id=user.id)
        city.save()
        user.save()
        place1.save()
        place2.save()

        response = self.client.get(f"/api/v1/cities/{city.id}/places")
        self.assertEqual(response.status_code, 200)
        # Check the response JSON for expected keys and values
        self.assertIn("Place 1", response.json[0]["name"])
        self.assertIn("Place 2", response.json[1]["name"])



if __name__ == "__main__":
    unittest.main()
