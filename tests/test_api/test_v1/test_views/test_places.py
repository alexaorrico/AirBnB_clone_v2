#!/usr/bin/python3
"""testing the index route"""
import unittest
import pep8
from os import getenv, environ
import requests
import json
from api.v1.app import *
from flask import request, jsonify
from models.place import Place
from models.city import City
from models.state import State
from models.user import User
from models import storage

class TestPlacesFunctions(unittest.TestCase):
    """Test the places class functions"""
    def test_get_place_by_city_id(self):
        """Test if it gets the place by city id or not"""
        if environ.get("HBNB_ENV") == 'test':
            with app.test_client() as client:
                state = State(name="Newland")
                state.save()
                city = City(name="Newcity", state_id=state.id)
                city.save()
                user = User(email="abc@123.com", password="chicken")
                user.save()
                place = Place(name="Becky's house",
                                  description="best house ever", number_rooms=3,
                                  number_bathrooms=1, max_guest=2,
                                  price_by_night=100, latitude=33.0,
                                  longitude=22.1, city_id=city.id,
                                  user_id=user.id)
                place.save()
                res = client.get('/api/v1/cities/{}/places'.format(city.id))
                self.assertEqual(res.status_code, 200)
                res1 = client.get('/api/v1/cities/{}/places/'.format(city.id))
                self.assertEqual(res.status_code, 200)

    def test_get_place_by_place_id(self):
        """Test if it gets the place by its id or not"""
        with app.test_client() as client:
            state = State(name="NewIrland")
            state.save()
            city = City(name="Irland", state_id=state.id)
            city.save()
            user = User(email="abc@123.com", password="chicken")
            user.save()
            place = Place(name="Becky's house",
                              description="best house ever", number_rooms=3,
                              number_bathrooms=1, max_guest=2,
                              price_by_night=100, latitude=33.0,
                              longitude=22.1, city_id=city.id,
                              user_id=user.id)
            place.save()
            res = client.get('/api/v1/places/{}'.format(place.id))
            self.assertEqual(res.status_code, 200)

    def test_delete_place_object(self):
        """Test if it deletes the place by id or not"""
        with app.test_client() as client:
            state = State(name="Brocklyin")
            state.save()
            city = City(name="Times", state_id=state.id)
            city.save()
            user = User(email="abc@123.com", password="chicken")
            user.save()
            place = Place(name="Becky's house",
                              description="best house ever", number_rooms=3,
                              number_bathrooms=1, max_guest=2,
                              price_by_night=100, latitude=33.0,
                              longitude=22.1, city_id=city.id,
                              user_id=user.id)
            place.save()
            res = client.get('api/v1/places/{}'.format(place.id))
            self.assertEqual(res.status_code, 200)
            res2 = client.delete('api/v1/places/{}'.format(place.id))
            self.assertEqual(res2.status_code, 200)
            res3 = client.get('api/v1/places/{}'.format(place.id))
            self.assertEqual(res3.status_code, 404)

    def test_create_place_obj_by_city_id(self):
        """Test if it creates place by the city id or not"""
        with app.test_client() as client:
            state = State(name="Newland")
            state.save()
            city = City(name="Denvor", state_id=state.id)
            city.save()
            user = User(email="abc@123.com", password="chicken")
            user.save()
            place = Place(name="Becky's house",
                              description="best house ever", number_rooms=3,
                              number_bathrooms=1, max_guest=2,
                              price_by_night=100, latitude=33.0,
                              longitude=22.1, city_id=city.id,
                              user_id=user.id)
            place.save()
            res = client.post('/api/v1/cities/{}/places'.format(city.id),
                          data=json.dumps(dict(name="Becky's Bakery",
                                               description="best egg tarts",
                                               number_rooms=3,
                                               number_bathrooms=1, max_guest=2,
                                               price_by_night=100,
                                               latitude=33.0, longitude=22.1,
                                               city_id=city.id,
                                               user_id=user.id)),
                          content_type="application/json")
            self.assertEqual(res.status_code, 201)

    def test_update_place(self):
        """Test if it updates a place by its id or not"""
        with app.test_client() as client:
            state = State(name="NewCity")
            state.save()
            city = City(name="Denvor", state_id=state.id)
            city.save()
            user = User(email="abc@123.com", password="chicken")
            user.save()
            place = Place(name="Becky's house",
                              description="best house ever", number_rooms=3,
                              number_bathrooms=1, max_guest=2,
                              price_by_night=100, latitude=33.0,
                              longitude=22.1, city_id=city.id,
                              user_id=user.id)
            place.save()
            res = client.put('api/v1/places/{}'.format(place.id),
                         data=json.dumps({"name": "Becky's Billards"}),
                         content_type="application/json")
            self.assertEqual(res.status_code, 200)


if __name__ == "__main__":
    unittest.main()
