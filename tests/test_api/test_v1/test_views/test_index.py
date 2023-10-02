#!/usr/bin/python3
"""testing the index route"""
import unittest
import pep8
from os import getenv
import requests
import json
from api.v1.app import *


storage = getenv("HBNB_TYPE_STORAGE")

class TestIndex(unittest.TestCase):
    """Test the index class"""
    def test_status(self):
        """Test if the status function return ok or not"""
        with app.test_client() as client:
            res = client.get('/api/v1/status')
            data = json.loads(res.data.decode('utf-8'))
            self.assertEqual(data, {"status": "OK"})

    def test_stats(self):
        """Test if the stats function return all
        the Classes count or not"""
        with app.test_client() as client:
            res = client.get('/api/v1/stats')
            data = json.loads(res.data.decode('utf-8'))
            for key, values in data.items():
                self.assertIsInstance(values, int)
                self.assertTrue(values >= 0)



if __name__ == "__main__":
    unittest.main()
