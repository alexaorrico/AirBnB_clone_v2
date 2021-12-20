#!/usr/bin/python3
"""Test the api states module"""
import unittest
from api.v1.app import app
from flask import Flask
from models import storage
from models.state import State
import json


class TestAPIAemnities(unittest.TestCase):
    """tests the app module"""
    @classmethod
    def setUpClass(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def testStatesGET(self):
        """tests the /api/v1/states route"""
        response = self.app.get('/api/v1/states')
        self.assertEqual(response.status_code, 200)

    def testStatesPOST(self):
        """tests POST for states"""
        start = storage.count('State')
        state_args = {"name": "Test", "id": "QO"}
        response = self.app.post(
            '/api/v1/states',
            content_type="application/json",
            data=json.dumps(state_args),
            follow_redirects=True)
        self.assertEqual(response.status_code, 201)
        end = storage.count('State')
        self.assertEqual(start + 1, end)

    def testSingleStateGET(self):
        """tests /api/v1/states/<state_id>"""
        # existing id
        st = State(name="Test")
        st.save()
        response = self.app.get('/api/v1/states/{}'.format(st.id))
        self.assertEqual(response.status_code, 200)
        # nonexistant id
        response = self.app.get('/api/v1/states/fake')
        self.assertEqual(response.status_code, 404)

    def testSingleStateDELETE(self):
        """tests /api/v1/states/<state_id>"""
        st = State(name="Test")
        st.save()
        response = self.app.delete('/api/v1/states/{}'.format(st.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(storage.get(State, st.id), None)

    def testSingleStatePUT(self):
        """tests /api/v1/states/<state_id>"""
        # with existing id and valid json
        am = State(name="Test")
        am.save()
        state_args = {"name": "Change", "id": "Don't change",
                      "created_at": "Don't Change"}
        am_id = am.id
        am_created_at = am.created_at
        response = self.app.put(
            '/api/v1/states/{}'.format(am.id),
            content_type="application/json",
            data=json.dumps(state_args),
            follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(am.name, "Change")
        self.assertEqual(am_id, am.id)
        self.assertEqual(am_created_at, am.created_at)
        # with existing id and no json
        response = self.app.put(
            '/api/v1/states/{}'.format(am.id))
        self.assertEqual(response.status_code, 400)
        # with nonexistant id
        response = self.app.put(
            '/api/v1/states/fake')
        self.assertEqual(response.status_code, 404)
