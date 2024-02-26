import unittest
from flask import json
from api.v1.app import app
from models import storage, state

State = state.State

class TestFlaskRoutes(unittest.TestCase):
    def setUp(self):
        # Initialize Flask app test client
        self.app = app.test_client()
        # Create test data
        self.state_data = {'name': 'Test State'}
        self.state = State(**self.state_data)
        storage.new(self.state)
        storage.save()

    def tearDown(self):
        # Reset the database after each test
        storage.delete(self.state)
        storage.save()

    def test_get_states(self):
        # Test case for retrieving all states
        response = self.app.get('/api/v1/states')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertTrue(isinstance(data, list))

    def test_get_state(self):
        # Test case for retrieving a specific state
        state = State(name="Test State")
        storage.new(state)
        storage.save()
        response = self.app.get(f'/api/v1/states/{state.id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['id'], state.id)
        # Test case for retrieving a non-existent state
        response = self.app.get('/api/v1/states/1000')
        self.assertEqual(response.status_code, 404)

    def test_delete_state(self):
        # Test case for deleting an existing state
        state = State(name="Test State")
        storage.new(state)
        storage.save()
        response = self.app.delete('/api/v1/states/{}'.format(state.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(storage.get('State', state.id), None)

        # Test case for deleting a non-existent state
        response = self.app.delete('/api/v1/states/1000')
        self.assertEqual(response.status_code, 404)

    def test_create_state(self):
        # Test case for creating a new state
        data = {'name': 'New State'}
        response = self.app.post('/api/v1/states', json=data)
        self.assertEqual(response.status_code, 201)
        state_id = json.loads(response.get_data(as_text=True))['id']
        self.assertTrue(storage.get('State', state_id))
        # Test case for creating a state with missing data
        response = self.app.post('/api/v1/states', json={})
        self.assertEqual(response.status_code, 400)

        # Test case for creating a state with invalid JSON
        response = self.app.post('/api/v1/states', json='invalid json')
        self.assertEqual(response.status_code, 400)

    def test_update_state(self):
        # Test case for updating an existing state
        state = State(name="Original State")
        storage.new(state)
        storage.save()
        data = {'name': 'Updated State'}
        response = self.app.put('/api/v1/states/{}'.format(state.id), json=data)
        self.assertEqual(response.status_code, 200)
        updated_state = storage.get('State', state.id)
        self.assertEqual(updated_state.name, 'Updated State')

        # Test case for updating a non-existent state
        response = self.app.put('/api/v1/states/1000', json=data)
        self.assertEqual(response.status_code, 404)

        # Test case for updating a state with invalid JSON
        response = self.app.put('/api/v1/states/{}'.format(state.id), json='invalid json')
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()
