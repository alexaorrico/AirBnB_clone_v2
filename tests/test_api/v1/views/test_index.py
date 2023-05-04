#!/usr/bin/python3
"""
Test cases for api redirections
"""
import unittest
from flask import Flask
from api.v1.app import app


class TestStatusRoutes(unittest.TestCase):
    """Tests for status routes"""
    @classmethod
    def setUpClass(self):
        """Set up for flask app request"""
        self.myapp = app.app_context()
        self.myapp.push()
        app.testing = True
        self.client = app.test_client()

    def test_status_code(self):
        """ Test for status """
        res = self.client.get('api/v1/status')
        self.assertEqual(res.status_code, 200)

    def test_content_type(self):
        """ Test return data """
        res = self.client.get('api/v1/status')
        self.assertEqual(res.content_type, 'application/json')


class TestStatsRoutes(unittest.TestCase):
    """ Test cases for Stats routes"""
    @classmethod
    def setUpClass(self):
        """Set up for flas app request"""
        self.myapp = app.app_context()
        self.myapp.push()
        app.testing = True
        self.client = app.test_client()

    def test_status_code(self):
        """ Test for status_code """
        res = self.client.get('api/v1/stats')
        self.assertEqual(res.status_code, 200)

    def test_content_type(self):
        """ Test for content-type """
        res = self.client.get('api/v1/stats')
        self.assertEqual(res.content_type, 'application/json')
