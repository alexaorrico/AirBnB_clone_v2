#!/usr/bin/python3
"""
testing api for flask App
"""
import unittest
import json
from flask import Flask

class TestFlaskApp(unittest.TestCase):
    """classes that have to be tested"""

    def setUp(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        app.config['DEBUG'] = False

        @app.route('/api/v1')
        def hello_world():
            return "Hello, World!"

        @app.route('/api/v1/info')
        def info():
            return {"version": "1.0", "name": "TestApp"}

        self.app = app.test_client()

    def test_hello_world(self):
        response = self.app.get('/api/v1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'Hello, World!')

    def test_info(self):
        response = self.app.get('/api/v1/info')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(data['name'], 'TestApp')
        self.assertEqual(data['version'], '1.0')

if __name__ == '__main__':
    unittest.main()