import unittest
from app import app


class TestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_index_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'Hello, World!')

    def test_not_found_route(self):
        response = self.app.get('/nothere')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {'error': 'Not found'})

if __name__ == '__main__':
    unittest.main()
