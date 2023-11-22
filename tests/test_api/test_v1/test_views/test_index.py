#!/usr/bin/python3
import unittest
from flask import Flask
from flask_testing import TestCase
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from main import app_views


class TestAppViews(TestCase):
    def create_app(self):
        app = Flask(__name__)
        app.register_blueprint(app_views)
        app.config['TESTING'] = True
        return app

    def test_get_status_route(self):
        response = self.client.get('/status')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'OK')

    def test_get_count_route(self):
        response = self.client.get('/stats')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['amenities'], len(Amenity.query.all()))
        self.assertEqual(response.json['cities'], len(City.query.all()))
        self.assertEqual(response.json['places'], len(Place.query.all()))
        self.assertEqual(response.json['reviews'], len(Review.query.all()))
        self.assertEqual(response.json['states'], len(State.query.all()))
        self.assertEqual(response.json['users'], len(User.query.all()))

if __name__ == '__main__':
    unittest.main()
