#!/usr/bin/python3
"""Test cases for State API endpoints"""

import unittest
from flask import json
from models import storage
from models.state import State
from api.v1.app import app

class TestStateAPI(unittest.TestCase):
    """Test API endpoints for State objects"""

    @classmethod
    def setUpClass(cls):
        """Set up test client"""
        cls.client = app.test_client()
        cls.client.testing = True

    def test_get_states(self):
        """Test GET /api/v1/states"""
        response = self.client.get('/api/v1/states')
        self.assertEqual(response.status_code, 200)

    def test_get_state(self):
        """Test GET /api/v1/states/<state_id>"""
        state = State(name="Test State")
        storage.new(state)
        storage.save()
        response = self.client.get(f'/api/v1/states/{state.id}')
        self.assertEqual(response.status_code, 200)

    def test_delete_state(self):
        """Test DELETE /api/v1/states/<state_id>"""
        state = State(name="Test State")
        storage.new(state)
        storage.save()
        response = self.client.delete(f'/api/v1/states/{state.id}')
        self.assertEqual(response.status_code, 200)

    def test_create_state(self):
        """Test POST /api/v1/states"""
        response = self.client.post('/api/v1/states', json={"name": "New State"})
        self.assertEqual(response.status_code, 201)

    def test_update_state(self):
        """Test PUT /api/v1/states/<state_id>"""
        state = State(name="Old State")
        storage.new(state)
        storage.save()
        response = self.client.put(f'/api/v1/states/{state.id}', json={"name": "Updated State"})
        self.assertEqual(response.status_code, 200)
