import unittest
import json
from api.v1.app import app

class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.index_response = '{"status":"OK"}\n'

    def test_index_route(self):
        response = self.app.get('/api/v1/status')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8'), self.index_response)

    # def test_not_found_error_handler(self):
    #     response = self.app.get('/nonexistent-route')
    #     self.assertEqual(response.status_code, 404)
    #     data = json.loads(response.data.decode('utf-8'))
    #     self.assertEqual(data['error'], 'Not found')

    # def test_bad_request_error_handler(self):
    #     response = self.app.get('/some-route-with-bad-request')
    #     self.assertEqual(response.status_code, 400)
    #     custom_message = response.data.decode('utf-8')
    #     self.assertIn('Bad Request', custom_message)

if __name__ == '__main__':
    unittest.main()
