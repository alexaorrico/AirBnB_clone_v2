#!/usr/bin/python3
"""testing the index route"""
import unittest
import pep8
from os import getenv
import requests
import json
from api.v1.app import *
from flask import request, jsonify
from models.state import State
from models.city import City
from models import storage

class TestCitiesFunctions(unittest.TestCase):
    """Test the cities class functions"""
    def test_get_city_by_state_id(self):
        """Test if it get the city by its state_id or not"""
        with app.test_client() as client:
            state = State(name="New York")
            state.save()
            city = City(name="Times", state_id=state.id)
            city.save()
            res = client.get('/api/v1/states/{}/cities'.format(state.id))
            self.assertEqual(res.status_code, 200)
            res1 = client.get('/api/v1/states/{}/cities/'.format(state.id))

    def test_get_city_by_city_id(self):
        """Test if it get the city by its id or not"""
        with app.test_client() as client:
            state = State(name="Afr")
            state.save()
            city = City(name="sou_Afr", state_id=state.id)
            city.save()
            res = client.get('/api/v1/states/{}/cities'.format(state.id))
            self.assertEqual(res.status_code, 200)

    def test_delete_city_object(self):
        """Test if it delete the city by its id or not"""
        with app.test_client() as client:
            state = State(name="Deanford")
            state.save()
            city = City(name="Maschesustis", state_id=state.id)
            city.save()
            res = client.get('api/v1/cities/{}'.format(city.id))
            self.assertEqual(res.status_code, 200)
            res2 = client.delete('api/v1/cities/{}'.format(city.id))
            self.assertEqual(res2.status_code, 200)
            res3 = client.get('api/v1/cities/{}'.format(city.id))
            self.assertEqual(res3.status_code, 404)

    def test_create_city_obj_by_state_id(self):
        """Test if it creates a city obj or not"""
        with app.test_client() as client:
            state = State(name="NewCity")
            state.save()
            city = City(name="Newland", state_id=state.id)
            city.save()
            res = client.post('/api/v1/states/{}/cities'.format(state.id),
                          data=json.dumps({"name": "Newsland"}),
                          content_type="application/json")
            self.assertEqual(res.status_code, 201)

    def test_update_city(self):
        """Test if it updates a city obj or not"""
        with app.test_client() as client:
            state = State(name="NewSite")
            state.save()
            city = City(name="Modernville", state_id=state.id)
            city.save()
            res = client.put('api/v1/cities/{}'.format(city.id),
                         data=json.dumps({"name": "Brokliyn"}),
                         content_type="application/json")
            self.assertEqual(res.status_code, 200)


if __name__ == "__main__":
    unittest.main()
