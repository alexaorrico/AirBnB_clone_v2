#!/usr/bin/python3
import unittest
from flask import json
from api.v1.app import app


class TestAmenitiesRoutes(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_get_all_amenities(self):
        response = self.app.get('/api/v1/amenities')
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(data, list))

    def test_get_amenity_by_id(self):
        amenity_id = '09e628ab-ebc3-4be8-baa4-2dbc844cec49'
        response = self.app.get(f'/api/v1/amenities/{amenity_id}')
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(data, dict))

    def test_get_nonexistent_amenity_by_id(self):
        response = self.app.get('/api/v1/amenities/nonexistent_id')
        self.assertEqual(response.status_code, 404)

    def test_create_amenity(self):
        payload = {'name': 'New Amenity', 'description': 'A new amenity'}
        response = self.app.post('/api/v1/amenities', data=json.dumps(payload), content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data.decode('utf-8'))
        self.assertTrue(isinstance(data, dict))


    def test_update_amenity(self):
        amenity_id = 'your_amenity_id'
        payload = {'name': 'Updated Amenity', 'description': 'An updated amenity'}
        response = self.app.put(f'/api/v1/amenities/{amenity_id}', data=json.dumps(payload), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode('utf-8'))
        self.assertTrue(isinstance(data, dict))

    def test_delete_amenity(self):
        amenity_id = 'your_amenity_id'
        response = self.app.delete(f'/api/v1/amenities/{amenity_id}')

        self.assertEqual(response.status_code, 204)


if __name__ == '__main__':
    unittest.main()
