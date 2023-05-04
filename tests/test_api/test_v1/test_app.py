#!/usr/bin/python3
"""
Testing app.py file
"""
import sys
from api.v1.app import app
import flask
import json
from models import storage
import unittest


class TestApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_404(self):
        rv = self.app.get('/bad')
        self.assertEqual(rv.status_code, 404)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")
        json_format = json.loads(str(rv.get_data(), encoding="utf-8"))
        self.assertEqual(json_format.get("error"), "Not found")


if __name__ == "__main__":
    unittest.main()
