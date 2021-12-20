#!/usr/bin/python3
"""Test the app module"""
import unittest
from api.v1.app import app
from flask import Flask


class TestApp(unittest.TestCase):
    """tests the app module"""
    @classmethod
    def setUpClass(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def testIsFlaskApp(self):
        """tests if app is a Flask instance"""
        self.assertIsInstance(app, Flask)

    def test_404(self):
        """tests 404 re-route"""
        response = self.app.get('/not/exist')
        self.assertEqual(response.status_code, 404)
        data = str(response.get_data(), encoding="utf-8")
        self.assertEqual(data, '{"error":"Not found"}\n')
