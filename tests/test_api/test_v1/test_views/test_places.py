#!/usr/bin/python3
'''testing the index route'''
import unittest
import pep8
from os import getenv
import requests
import json
from api.v1.app import *
from flask import request, jsonify
from models.place import Place
from models.city import City
from models.state import State
from models.user import User
from models import storage


class TestPlaces(unittest.TestCase):
    '''test city'''
    def test_lists_places_of_city(self):
        '''test places GET route'''
        with app.test_client() as c:
            new_state = State(name="Beckystan")
            storage.new(new_state)
            new_city = City(name="Chensville", state_id=new_state.id)
            storage.new(new_city)
            new_user = User(email="abc@123.com", password="chicken")
            storage.new(new_user)
            new_place = Place(name="Becky's Bathhouse",
                              description="best bath ever", number_rooms=3,
                              number_bathrooms=0, max_guest=2,
                              price_by_night=100, latitude=33.0,
                              longitude=22.1, city_id=new_city.id,
                              user_id=new_user.id)
            storage.new(new_place)
            resp = c.get('/api/v1/cities/{}/places'.format(new_city.id))
            self.assertEqual(resp.status_code, 200)
            resp2 = c.get('/api/v1/cities/{}/places/'.format(new_city.id))
            self.assertEqual(resp.status_code, 200)

    def test_create_place(self):
        '''test place POST route'''
        with app.test_client() as c:
            new_state = State(name="Beckystan")
            storage.new(new_state)
            new_city = City(name="Chensville", state_id=new_state.id)
            storage.new(new_city)
            new_user = User(email="abc@123.com", password="chicken")
            storage.new(new_user)
            new_place = Place(name="Becky's Bathhouse",
                              description="best bath ever", number_rooms=3,
                              number_bathrooms=0, max_guest=2,
                              price_by_night=100, latitude=33.0,
                              longitude=22.1, city_id=new_city.id,
                              user_id=new_user.id)
            storage.new(new_place)
            resp = c.post('/api/v1/cities/{}/places'.format(new_city.id),
                          data=json.dumps(dict(name="Becky's Bakery",
                                               description="best egg tarts",
                                               number_rooms=3,
                                               number_bathrooms=0, max_guest=2,
                                               price_by_night=100,
                                               latitude=33.0, longitude=22.1,
                                               city_id=new_city.id,
                                               user_id=new_user.id)),
                          content_type="application/json")
            # data = json.loads(resp.data.decode('utf-8'))
            # print(data)
            self.assertEqual(resp.status_code, 201)

    def test_delete_place(self):
        '''test place DELETE route'''
        with app.test_client() as c:
            new_state = State(name="Beckystan")
            storage.new(new_state)
            new_city = City(name="Chensville", state_id=new_state.id)
            storage.new(new_city)
            new_user = User(email="abc@123.com", password="chicken")
            storage.new(new_user)
            new_place = Place(name="Becky's Bathhouse",
                              description="best bath ever", number_rooms=3,
                              number_bathrooms=0, max_guest=2,
                              price_by_night=100, latitude=33.0,
                              longitude=22.1, city_id=new_city.id,
                              user_id=new_user.id)
            storage.new(new_place)
            resp = c.get('api/v1/places/{}'.format(new_place.id))
            self.assertEqual(resp.status_code, 200)
            resp1 = c.delete('api/v1/places/{}'.format(new_place.id))
            self.assertEqual(resp1.status_code, 404)
            resp2 = c.get('api/v1/places/{}'.format(new_place.id))
            self.assertEqual(resp2.status_code, 404)

    def test_get_place(self):
        '''test place GET by id route'''
        with app.test_client() as c:
            new_state = State(name="Beckystan")
            storage.new(new_state)
            new_city = City(name="Chensville", state_id=new_state.id)
            storage.new(new_city)
            new_user = User(email="abc@123.com", password="chicken")
            storage.new(new_user)
            new_place = Place(name="Becky's Bathhouse",
                              description="best bath ever", number_rooms=3,
                              number_bathrooms=0, max_guest=2,
                              price_by_night=100, latitude=33.0,
                              longitude=22.1, city_id=new_city.id,
                              user_id=new_user.id)
            storage.new(new_place)
            resp = c.get('/api/v1/cities/{}/places'.format(new_city.id))
            self.assertEqual(resp.status_code, 200)

    def test_update_place(self):
        '''test place PUT route'''
        with app.test_client() as c:
            new_state = State(name="Beckystan")
            storage.new(new_state)
            new_city = City(name="Chensville", state_id=new_state.id)
            storage.new(new_city)
            new_user = User(email="abc@123.com", password="chicken")
            storage.new(new_user)
            new_place = Place(name="Becky's Bathhouse",
                              description="best bath ever", number_rooms=3,
                              number_bathrooms=0, max_guest=2,
                              price_by_night=100, latitude=33.0,
                              longitude=22.1, city_id=new_city.id,
                              user_id=new_user.id)
            storage.new(new_place)
            resp = c.put('api/v1/places/{}'.format(new_place.id),
                         data=json.dumps({"name": "Becky's Billards"}),
                         content_type="application/json")
            # data = json.loads(resp.data.decode('utf-8'))
            # print(data)
            self.assertEqual(resp.status_code, 200)


if __name__ == '__main__':
    unittest.main()
