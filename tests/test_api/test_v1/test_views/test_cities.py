#!/usr/bin/python3
"""
This files Contains tests for views cities routes
"""

import unittest

from api.v1.app import app
from models import storage
from models.city import City
from models.state import State


class TestViewsCity(unittest.TestCase):
    """Test Class for Views City routes
    """

    def setUp(self):
        """Sets up the flask app for testing"""
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()
        self.state = State(name="Ethiopia")
        self.city_1 = City(name="Addis Ababa", state_id=self.state.id)
        self.city_2 = City(name="Harar", state_id=self.state.id)
        storage.new(self.state)
        storage.new(self.city_1)
        storage.new(self.city_2)
        storage.save()

    def tearDown(self):
        """Removes the flask app context"""
        storage.delete(self.state)
        storage.delete(self.city_1)
        storage.delete(self.city_2)
        storage.save()
        self.ctx.pop()

    def test_state_cities_endpoint(self):
        """Tests the /states/<state_id>/cities endpoint returns list of cities
        """
        response = self.client.get(
            "/api/v1/states/{}/cities".format(self.state.id), )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        data = list(response.get_json())
        result = filter(
            lambda city: city["id"] == self.city_1.id,
            data,
        )
        self.assertIsNotNone(next(result))
