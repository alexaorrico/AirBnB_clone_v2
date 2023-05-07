#!/usr/bin/python3
"""
Contains tests for views place reviews routes
"""

import unittest

from api.v1.app import app
from models import storage
from models.city import City
from models.place import Place
from models.state import State
from models.user import User


class TestViewsPlaceReviews(unittest.TestCase):
    """Test Class for Views Place Reviews routes
    """

    def setUp(self):
        """Sets up the flask app for testing"""
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()
        self.state = State(name="Ethiopia")
        self.city = City(name="Addis Ababa", state_id=self.state.id)
        self.user = User(email="abebe@example.com", password="12345")
        self.place_1 = Place(
            name="Sweet Home",
            user_id=self.user.id,
            city_id=self.city.id,
        )
        self.place_2 = Place(
            name="Entoto Park",
            user_id=self.user.id,
            city_id=self.city.id,
        )
        storage.new(self.state)
        storage.new(self.city)
        storage.new(self.user)
        storage.new(self.place_1)
        storage.new(self.place_2)
        storage.save()

    def tearDown(self):
        """Removes the flask app context"""
        storage.delete(self.state)
        storage.delete(self.city)
        storage.delete(self.user)
        storage.delete(self.place_1)
        storage.delete(self.place_2)
        storage.save()
        self.ctx.pop()

    def test_places_endpoint(self):
        """Tests the /cities/<city_id>/places endpoint returns list of places
        """
        response = self.client.get(
            "/api/v1/cities/{}/places".format(self.city.id), )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        data = list(response.get_json())
        result = filter(
            lambda place: place["id"] == self.place_1.id,
            data,
        )
        self.assertIsNotNone(next(result))
