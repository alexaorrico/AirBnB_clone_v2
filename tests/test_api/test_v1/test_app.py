#!/usr/bin/python3
"""
Test model for api app
"""
import json
import unittest
from unittest import mock
from api.v1.app import app


class TestAPIApp(unittest.TestCase):
    """Test the app creation and some general functionalties"""
    @mock.patch('models.storage.close')
    def test_calling_storageClose(self, mocked_close):
        """Test calling the storage.close method after request
           tear down"""
        with app.test_clien() as tester:
            tester.head('/')
        self.assertTrue(mocked_close.called)

    def test_404_statusCode(self):
        """Test the  response code of a not found request"""
        testter = app.test_client()
        res = testter.get('/nop')

        self.assertEqual(res.status_code, 404)

    def test_404_content_type(self):
        """Test the  response code of a not found request"""
        testter = app.test_client()
        res = testter.get('/nop')

        self.assertEqual(res.content_type, "application/json")

    def test_404_content(self):
        """Test the  response code of a not found request"""
        message = {"error": "Not found"}
        testter = app.test_client()
        res = testter.get('/nop')

        self.assertDictEqual(json.loads(res.to_json()), message)
