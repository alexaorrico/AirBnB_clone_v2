#!/usr/bin/python3
'''testing the index route'''
import unittest
import pep8
from os import getenv
import requests
import json
from api.v1.app import *


storage = getenv("HBNB_TYPE_STORAGE")


class TestIndex(unittest.TestCase):
    '''test index'''
    def test_status(self):        
        '''test status function'''
        with app.test_client() as c:
            resp = c.get('/api/v1/status')
            data = json.loads(resp.data.decode('utf-8'))
            self.assertEqual(data, {'status': 'OK'})


    def test_count(self):
        '''test count'''
        with app.test_client() as c:
            resp = c.get('/api/v1/stats')
            data = json.loads(resp.data.decode('utf-8'))
            for k, v in data.items():
                self.assertIsInstance(v, int)
                self.assertTrue(v >= 0)

    def test_404(self):
        '''test for 404 error'''
        with app.test_client() as c:
            resp = c.get('/api/v1/yabbadabbadoo')
            data = json.loads(resp.data.decode('utf-8'))
            self.assertEqual(data, {"error": "Not found"})


if __name__ == '__main__':
    unittest.main()
