#!/usr/bin/python3
"""
Contains tests for views place reviews routes
"""

import unittest

from api.v1.app import app
from models import storage
from models.city import City
from models.place import Place
from models.review import Review
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
        self.user_1 = User(email="abebe@example.com", password="12345")
        self.user_2 = User(email="alemitu@example.com", password="12345")
        self.place = Place(
            name="Sweet Home",
            user_id=self.user_1.id,
            city_id=self.city.id,
        )
        self.review_1 = Review(
            text="awesome place",
            user_id=self.user_1.id,
            place_id=self.place.id,
        )
        self.review_2 = Review(
            text="loved it",
            user_id=self.user_2.id,
            place_id=self.place.id,
        )
        storage.new(self.state)
        storage.new(self.city)
        storage.new(self.user_1)
        storage.new(self.user_2)
        storage.new(self.place)
        storage.new(self.review_1)
        storage.new(self.review_2)
        storage.save()

    def tearDown(self):
        """Removes the flask app context"""
        storage.delete(self.state)
        storage.delete(self.city)
        storage.delete(self.user_1)
        storage.delete(self.user_2)
        storage.delete(self.place)
        storage.delete(self.review_1)
        storage.delete(self.review_2)
        storage.save()
        self.ctx.pop()

    def test_place_reviews_endpoint(self):
        """Tests the /places/<place_id>/reviews endpoint returns list of
        reviews
        """
        response = self.client.get(
            "/api/v1/places/{}/reviews".format(self.place.id), )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        data = list(response.get_json())
        result = filter(
            lambda review: review["id"] == self.review_1.id,
            data,
        )
        self.assertIsNotNone(next(result))
