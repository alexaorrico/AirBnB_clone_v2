#!/usr/bin/python3
"""
This files Contains tests for views amenities routes
"""

import unittest

from api.v1.app import app
from models import storage
from models.amenity import Amenity


class TestViewsAmenity(unittest.TestCase):
    """Test Class for Views Amenity routes
    """

    def setUp(self):
        """Sets up the flask app for testing"""
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()
        self.amenity_1 = Amenity(name="Wi-Fi")
        self.amenity_2 = Amenity(name="TV")
        storage.new(self.amenity_1)
        storage.new(self.amenity_2)
        storage.save()

    def tearDown(self):
        """Removes the flask app context"""
        storage.delete(self.amenity_1)
        storage.delete(self.amenity_2)
        storage.save()
        self.ctx.pop()

    def test_amenities_endpoint(self):
        """Tests the /amenities endpoint returns list of amenities"""
        response = self.client.get("/api/v1/amenities")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        data = list(response.get_json())
        result = filter(
            lambda amenity: amenity["id"] == self.amenity_1.id,
            data,
        )
        self.assertIsNotNone(next(result))
