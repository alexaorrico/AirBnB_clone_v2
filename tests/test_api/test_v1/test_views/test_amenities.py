#!/usr/bin/python3
"""testing the index route"""
import unittest
import pep8
from os import getenv
import requests
import json
from api.v1.app import *
from flask import request, jsonify
from models.amenity import Amenity
from models import storage

class TestAmenitiesFunctions(unittest.TestCase):
    """Test the amenities class functions"""
    def test_get_all_amenity(self):
        """Test if it get all amenities or not"""
        with app.test_client() as client:
            res = client.get('/api/v1/amenities')
            self.assertEqual(res.status_code, 200)
            res1 = client.get('/api/v1/amenities/')
            self.assertEqual(res.status_code, 200)

    def test_get_amenity_based_on_id(self):
        """Test if it get smenity obj by its id or not"""
        with app.test_client() as client:
            amenity = Amenity(name="3 meals a day")
            amenity.save()
            res = client.get('api/v1/amenities/{}'.format(amenity.id))
            self.assertEqual(res.status_code, 200)

    def test_delete_amenity_object(self):
        """Test if it deletes the amenity obj by its id or not"""
        with app.test_client() as client:
            amenity = Amenity(name="3 meals a day")
            amenity.save()
            res = client.get('api/v1/amenities/{}'.format(amenity.id))
            self.assertEqual(res.status_code, 200)
            res2 = client.delete('api/v1/amenities/{}'.format(amenity.id))
            self.assertEqual(res2.status_code, 200)
            res3 = client.get('api/v1/amenities/{}'.format(amenity.id))
            self.assertEqual(res3.status_code, 404)

    def test_create_amenity_object(self):
        """Test if it creates an amenity obj or not"""
        with app.test_client() as client:
            res = client.post('/api/v1/amenities/',
                          data=json.dumps({"name": "trees"}),
                          content_type="application/json")
            self.assertEqual(res.status_code, 201)

    def test_update_amenity(self):
        """Test if it updates an amenity obj or not"""
        with app.test_client() as client:
            amenity = Amenity(name="3 meals a day")
            amenity.save()
            res = client.put('api/v1/amenities/{}'.format(amenity.id),
                         data=json.dumps({"name": "4 meals a day"}),
                         content_type="application/json")
            self.assertEqual(res.status_code, 200)


if __name__ == "__main__":
    unittest.main()
