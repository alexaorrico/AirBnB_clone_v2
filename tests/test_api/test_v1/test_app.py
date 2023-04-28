#!/usr/bin/python3
"""Tests for the module api.v1.app"""

import unittest
from werkzeug.test import Client
from api.v1 import app

class AppTestCase(unittest.TestCase):
    """Class for Testing the module app"""
    def test_app_application(self):
        """Tests the app using Client"""
        c = Client(app.app)
        response = c.get('/api/v1/status')
        self.assertEqual(response.status_code, 200)

    def test_app_response_content_type(self):
        """Tests the response content type"""
        c = Client(app.app)
        response = c.get('/api/v1/status')
        content_type = response.headers.get('Content-Type')
        self.assertEqual(content_type, 'application/json')
