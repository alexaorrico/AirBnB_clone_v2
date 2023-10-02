# tests/test_amenities.py

import unittest
from flask import Flask
from api.v1.views import app_views
from models import storage, Amenity

class TestAmenitiesRoute(unittest.TestCase):
    """Test cases for the Amenities view."""

    def setUp(self):
        """Set up the test environment."""
        self.app = Flask(__name__)
        app_views.app.config["TESTING"] = True
        self.client = app_views.app.test_client()

    def tearDown(self):
        """Tear down the test environment."""
        storage.close()

    def test_get_amenities_route(self):
        """Test the /amenities route (GET)."""
        # Create and save some Amenity objects for testing
        amenity1 = Amenity(name="Amenity 1")
        amenity2 = Amenity(name="Amenity 2")
        amenity1.save()
        amenity2.save()

        response = self.client.get("/api/v1/amenities")
        self.assertEqual(response.status_code, 200)
        # Check response JSON for expected keys and values
        self.assertIn("Amenity 1", response.json)
        self.assertIn("Amenity 2", response.json)



if __name__ == "__main__":
    unittest.main()
