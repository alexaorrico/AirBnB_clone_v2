"""
API Test module
"""
import re
import unittest
import requests

class TestErrorHandling(unittest.TestCase):
    def setUp(self):
        """
        makes a get requests an returns a response
        """
        res = requests.get('http://0.0.0.0:5000/api/v1/nop')
        return res
    
    def test_response(self):
        """
        test response object returned
        """
        res = self.setUp()
        self.assertDictEqual(res.json(), {'error': 'Not Found'})
    
    def test_response_code(self):
        """
        test status code returned
        """
        res = self.setUp()
        self.assertEqual(res.status_code, 404)

    def test_content_type(self):
        """
        test content_type returned
        """
        res = self.setUp()
        self.assertEqual(res.headers['content-type'], 'application/json')

class TestStates(unittest.TestCase):
    pass