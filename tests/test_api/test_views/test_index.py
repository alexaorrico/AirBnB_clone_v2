#!/usr/bin/python3
"""This module contains test cases for stats."""

from api.v1.app import app
from flask import json
import unittest
from models import storage


class TestStatsCounts(unittest.TestCase):
    """test case for stats."""

    def setUp(self):
        """setting up the client."""
        self.app = app.test_client()

    def test_stats_counts(self):
        """test stats."""
        response = self.app.get('/api/v1/stats')
        data = json.loads(response.data.decode('utf-8'))

        amenities_count = storage.count('Amenity')
        cities_count = storage.count('City')
        places_count = storage.count('Place')
        reviews_count = storage.count('Review')
        states_count = storage.count('State')
        users_count = storage.count('User')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['amenities'], amenities_count)
        self.assertEqual(data['cities'], cities_count)
        self.assertEqual(data['places'], places_count)
        self.assertEqual(data['reviews'], reviews_count)
        self.assertEqual(data['states'], states_count)
        self.assertEqual(data['users'], users_count)

    def test_stats_response_status(self):
        """testing response status."""
        response = self.app.get('/api/v1/stats')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
