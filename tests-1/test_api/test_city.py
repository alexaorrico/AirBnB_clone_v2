#!/usr/bin/python3
from api.v1.app import app as app
from flask import Flask, make_response, jsonify, json
import unittest
import pprint
import ast
import os

@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                    "Testing FileStorage")
class FlaskTestCase(unittest.TestCase):
    data = {"name": "California"}
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.app = app
# test correct status code
    def test_post_methoc(self):
        tester = app.test_client(self)
        response = tester.post('/api/v1/states', json=self.data)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.status_code, 201)


    def test_get_method_by_id(self):
        tester = app.test_client(self)
        response = tester.post('/api/v1/states', json=self.data)
        response = tester.post('/api/v1/states', json=self.data)
        all_places = tester.get('/api/v1/states')
        self.assertEqual(all_places.status_code, 200)
        data1 = all_places.data.decode('UTF-8')
        all_places = ast.literal_eval(data1)
        dic_get = all_places
        unique_id = dic_get[-1]['id']
        arguments = {"name": "lima"}

        tester = app.test_client(self)
        response = tester.post('/api/v1/states/{}/cities'.format(unique_id), json=arguments)
        self.assertEqual(response.status_code, 201)
        data1 = response.data.decode('UTF-8')
        mydata = ast.literal_eval(data1)
        dic_by_id = mydata

        response = tester.get('/api/v1/states/{}/cities'.format(unique_id))
        self.assertEqual(response.status_code, 200)
        data1 = response.data.decode('UTF-8')
        mydata = ast.literal_eval(data1)
        dic_by_id = mydata
        city_id = dic_by_id[-1]['id']

        response = tester.get('/api/v1/cities/{}'.format(city_id))
        self.assertEqual(response.status_code, 200)
        data1 = response.data.decode('UTF-8')
        mydata = ast.literal_eval(data1)
        dic_by_id = mydata
        city_id = dic_by_id['id']

        response = tester.put('/api/v1/cities/{}'.format(city_id), json={'name': 'CALLAO'})
        self.assertEqual(response.status_code, 200)
        data1 = response.data.decode('UTF-8')
        mydata = ast.literal_eval(data1)
        dic_by_id = mydata

if __name__ == "__main__":

    unnittest.main()
