import unittest
import json
from models.state import State
from api.v1.app import app
from models import storage
from flask import Response


class TestAppViews(unittest.TestCase):
    def setUp(self):
        # Create a test client
        self.app = app.test_client()
        # Create a new state for testing
        self.test_state = State(name="Test State")
        self.test_state.save()

    def tearDown(self):
        # Clean up the test state after each test
        self.test_state.delete()

    def test_get_states(self):
        response = self.app.get('/api/v1/states')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertTrue(isinstance(data, list))

    def test_get_states_id(self):
        response = self.app.get('/api/v1/states/{}'.format(self.test_state.id))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['id'], self.test_state.id)

    def test_get_states_id_not_found(self):
        response = self.app.get('/api/v1/states/12345')  # Non-existing ID
        self.assertEqual(response.status_code, 404)

    def test_del_by_id(self):
        response = self.app.delete(
            '/api/v1/states/{}'.format(self.test_state.id))
        self.assertEqual(response.status_code, 200)
        # Verify that the state has been deleted
        deleted_state = storage.get(State, self.test_state.id)
        self.assertIsNone(deleted_state)

    def test_del_by_id_not_found(self):
        response = self.app.delete('/api/v1/states/12345')  # Non-existing ID
        self.assertEqual(response.status_code, 404)

    def test_create_state(self):
        new_state_data = {"name": "New State"}
        response = self.app.post('/api/v1/states', json=new_state_data)
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.get_data(as_text=True))
        self.assertIn('id', data)
        self.assertEqual(data['name'], new_state_data['name'])

    def test_create_state_missing_name(self):
        invalid_state_data = {"other_key": "value"}
        response = self.app.post('/api/v1/states', json=invalid_state_data)
        self.assertEqual(response.status_code, 400)

    def test_update_state(self):
        updated_state_data = {"name": "Updated State"}
        response = self.app.put(
            '/api/v1/states/{}'.format(self.test_state.id), json=updated_state_data)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['name'], updated_state_data['name'])

    def test_update_state_not_found(self):
        response = self.app.put(
            '/api/v1/states/12345',
            json={
                "name": "Updated State"})
        self.assertEqual(response.status_code, 404)

    def test_update_state_invalid_json(self):
        response = self.app.put(
            '/api/v1/states/{}'.format(
                self.test_state.id),
            data="Invalid JSON",
            content_type="application/json")
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()
