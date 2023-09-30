#!/usr/bin/python3
import unittest
from flask import Flask, json
from api.v1.app import app
from models.state import State
from models import storage

class TestStates(unittest.TestCase):

    def setUp(self):
        """
        Setup
        """
        self.app = app.test_client()
        self.test_state = {"name": "TestState"}

    def test_get_states(self):
        """Test retrieving list of states."""
        response = self.app.get('/states')
        self.assertEqual(response.status_code, 200)

    def test_get_state_by_id(self):
        """Test retrieving a specific state."""
        new_state = State(**self.test_state)
        new_state.save()
        response = self.app.get('/states/{}'.format(new_state.id))
        self.assertEqual(response.status_code, 200)
        storage.delete(new_state)
        storage.save()

    def test_404_state(self):
        """Test for non-existing state."""
        response = self.app.get('/states/54254')
        self.assertEqual(response.status_code, 404)

    def test_create_state(self):
        """Test creating a state."""
        response = self.app.post('/states', data=json.dumps(self.test_state),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 201)
        state_data = json.loads(response.data)
        storage.delete(State(**state_data))
        storage.save()

if __name__ == "__main__":
    unittest.main()
