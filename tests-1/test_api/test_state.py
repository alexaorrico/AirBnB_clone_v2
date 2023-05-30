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
    def test_get_status(self):
        tester = app.test_client(self)
        response = tester.get('/api/v1/states', content_type='html/text')
        self.assertEqual(response.status_code, 200)
    def test_valid_json(self):
        tester = app.test_client(self)
        response = tester.get('/api/v1/states', content_type='html/text')
        self.assertEqual(response.content_type, 'application/json')


    def test_post_methoc(self):
        tester = app.test_client(self)
        response = tester.post('/api/v1/states', json=self.data)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.status_code, 201)

    def test_get_post_method(self):
        tester = app.test_client(self)
        response = tester.post('/api/v1/states', json=self.data)
        data1 = response.data.decode('UTF-8')
        mydata = ast.literal_eval(data1)
        dic = mydata
        self.assertTrue("name" in dic)
        self.assertTrue("__class__" in dic)
        self.assertTrue("created_at" in dic)
        self.assertTrue("id" in dic)
        self.assertTrue("updated_at" in dic)
        response = tester.get('/api/v1/states')
        data1 = response.data.decode('UTF-8')
        mydata = ast.literal_eval(data1)
        dic = mydata[0]
        self.assertTrue("name" in dic)
        self.assertTrue("__class__" in dic)
        self.assertTrue("created_at" in dic)
        self.assertTrue("id" in dic)
        self.assertTrue("updated_at" in dic)


    def test_get_method_by_id(self):
        tester = app.test_client(self)
        response = tester.post('/api/v1/states', json=self.data)
        self.assertEqual(response.status_code, 201)
        data1 = response.data.decode('UTF-8')
        mydata = ast.literal_eval(data1)
        dic_post = mydata

        all_places = tester.get('/api/v1/states')
        self.assertEqual(all_places.status_code, 200)
        data1 = all_places.data.decode('UTF-8')
        all_places = ast.literal_eval(data1)
        dic_get = all_places

        unique_id = dic_get[-1]['id']

        state_id = {"id": unique_id}
        tester = app.test_client(self)
        response = tester.get('/api/v1/states/{}'.format(unique_id))
        self.assertEqual(response.status_code, 200)
        data1 = response.data.decode('UTF-8')
        mydata = ast.literal_eval(data1)
        dic_by_id = mydata

    def test_put_method_by_id(self):
        tester = app.test_client(self)
        all_places = tester.get('/api/v1/states')
        self.assertEqual(all_places.status_code, 200)
        data1 = all_places.data.decode('UTF-8')
        all_places = ast.literal_eval(data1)
        dic_get = all_places

        unique_id = dic_get[0]['id']
        arguments_need = {"name": "Updating"}
        tester = app.test_client(self)
        response = tester.put('/api/v1/states/{}'.format(unique_id), json=arguments_need)
        self.assertEqual(response.status_code, 200)
        data1 = response.data.decode('UTF-8')
        mydata = ast.literal_eval(data1)
        dic_by_id = mydata
        self.assertTrue("Updating" in dic_by_id['name'])
        self.assertTrue("__class__" in dic_by_id)
        self.assertTrue("created_at" in dic_by_id)
        self.assertTrue("id" in dic_by_id)
        self.assertTrue("updated_at" in dic_by_id)


if __name__ == "__main__":

    unnittest.main()
