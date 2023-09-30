#!/usr/bin/python3
import unittest
from flask import Flask
from api.v1.app import app

class TestApp(unittest.TestCase):

    def setUp(self):
        """
        Setup tests
        """
        self.app = app.test_client()

    def test_404(self):
        """
        Test 404
        """
        response = self.app.get('/unknown_route')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"Not found", response.data)

if __name__ == "__main__":
    unittest.main()
