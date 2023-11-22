#!/usr/bin/python3
import unittest
from api.v1.app import app


class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_error_handler_404(self):
        response = self.app.get('/nonexistent_route')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {"error": "Not found"})

    def test_teardown_appcontext(self):
        with app.app_context():
            with self.assertRaises(Exception):
                app.teardown_appcontext(Exception())

    def test_app_views_blueprint(self):
        self.assertEqual(len(app.blueprints), 1)
        self.assertIn('app_views', app.blueprints)

    def test_app_run(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
