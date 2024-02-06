import unittest
from api.v1.views.cities import app_views
from flask import jsonify
from models.state import State
from models.city import City
from models import storage
from unittest.mock import patch


class TestCitiesView(unittest.TestCase):
    def setUp(self):
        self.client = app_views.test_client()

    def tearDown(self):
        storage.delete_all()

    def test_get_cities(self):
        with patch('flask.request') as mock_request:
            mock_request.method = 'GET'
            state = State(name='California')
            state.save()
            city = City(name='Los Angeles', state_id=state.id)
            city.save()
            response = self.client.get(f'/states/{state.id}/cities')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.get_json(), [city.to_dict()])

    def test_get_cities_invalid_state(self):
        with patch('flask.request') as mock_request:
            mock_request.method = 'GET'
            response = self.client.get('/states/invalid_state_id/cities')
            self.assertEqual(response.status_code, 404)

    def test_post_cities(self):
        with patch('flask.request') as mock_request:
            mock_request.method = 'POST'
            mock_request.json = {'name': 'San Francisco'}
            state = State(name='California')
            state.save()
            response = self.client.post(f'/states/{state.id}/cities')
            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.get_json(), {'name': 'San Francisco', 'state_id': state.id})

    def test_post_cities_invalid_state(self):
        with patch('flask.request') as mock_request:
            mock_request.method = 'POST'
            mock_request.json = {'name': 'San Francisco'}
            response = self.client.post('/states/invalid_state_id/cities')
            self.assertEqual(response.status_code, 404)

    def test_post_cities_missing_name(self):
        with patch('flask.request') as mock_request:
            mock_request.method = 'POST'
            mock_request.json = {}
            state = State(name='California')
            state.save()
            response = self.client.post(f'/states/{state.id}/cities')
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.get_json(), {'error': 'Missing name'})

    def test_post_cities_not_json(self):
        with patch('flask.request') as mock_request:
            mock_request.method = 'POST'
            mock_request.json = None
            state = State(name='California')
            state.save()
            response = self.client.post(f'/states/{state.id}/cities')
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.get_json(), {'error': 'Not a JSON'})

    def test_put_cities(self):
        with patch('flask.request') as mock_request:
            mock_request.method = 'PUT'
            mock_request.json = {'name': 'San Francisco'}
            state = State(name='California')
            state.save()
            city = City(name='Los Angeles', state_id=state.id)
            city.save()
            response = self.client.put(f'/cities/{city.id}')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.get_json(), {'name': 'San Francisco', 'state_id': state.id})

    def test_put_cities_invalid_city(self):
        with patch('flask.request') as mock_request:
            mock_request.method = 'PUT'
            mock_request.json = {'name': 'San Francisco'}
            response = self.client.put('/cities/invalid_city_id')
            self.assertEqual(response.status_code, 404)

    def test_put_cities_not_json(self):
        with patch('flask.request') as mock_request:
            mock_request.method = 'PUT'
            mock_request.json = None
            state = State(name='California')
            state.save()
            city = City(name='Los Angeles', state_id=state.id)
            city.save()
            response = self.client.put(f'/cities/{city.id}')
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.get_json(), {'error': 'Not a JSON'})

    def test_delete_cities(self):
        with patch('flask.request') as mock_request:
            mock_request.method = 'DELETE'
            state = State(name='California')
            state.save()
            city = City(name='Los Angeles', state_id=state.id)
            city.save()
            response = self.client.delete(f'/cities/{city.id}')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.get_json(), {})

    def test_delete_cities_invalid_city(self):
        with patch('flask.request') as mock_request:
            mock_request.method = 'DELETE'
            response = self.client.delete('/cities/invalid_city_id')
            self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()