# tests/test_app.py

import unittest
from flask import Flask
from api.v1.app import app
from models import storage,City, Place, Amenity

class TestApp(unittest.TestCase):
    """Test cases for the Flask application."""

    def setUp(self):
        """Set up the test environment."""
        self.app = app.test_client()

    def tearDown(self):
        """Tear down the test environment."""
        pass     

    def test_hello_world_route(self):
        """Test the / route (hello world)."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode("utf-8"), "Hello, World!")


    def test_status_route(self):
        """Test the /status route."""
        response = self.client.get("/api/v1/status")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"status": "OK"})


    def test_stats_route(self):
        """Test the /stats route."""
        # Simulate adding objects to storage for testing
        storage.create(Amenity(name="TestAmenity"))
        storage.create(City(name="TestCity"))
        storage.create(Place(name="TestPlace"))
        
        response = self.client.get("/api/v1/stats")
        self.assertEqual(response.status_code, 200)
        # Check response JSON for expected keys and values
        self.assertIn("Amenity", response.json)
        self.assertIn("City", response.json)
        self.assertIn("Place", response.json)    

    def test_404_error_handler(self):
        """Test the 404 error handler."""
        response = self.app.get("/non_existent_route")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {"error": "Not found"})

if __name__ == "__main__":
    unittest.main()
