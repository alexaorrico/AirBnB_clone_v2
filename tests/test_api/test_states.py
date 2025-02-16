import unittest
import json
from api.v1.app import app

class TestStateAPI(unittest.TestCase):
    def setUp(self):
        """Set up test client"""
        self.client = app.test_client()

    def test_get_states(self):
        """Test GET request to /api/v1/states"""
        response = self.client.get('/api/v1/states')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

if __name__ == '__main__':
    unittest.main()

