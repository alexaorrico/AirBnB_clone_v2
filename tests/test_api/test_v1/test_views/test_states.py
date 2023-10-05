#!/usr/bin/python3
'''testing the index route'''
import unittest
import pep8
from os import getenv
import requests
import json
from api.v1.app import *
from flask import request, jsonify
from models.state import State
from models import storage

class Teststatesfunctions(unittest.TestCase):
    """Test the functions of the states"""
    def test_get_states(self):
        """Test if it return all the states or not"""
        with app.test_client() as client:
            res = client.get('/api/v1/states')
            self.assertEqual(res.status_code, 200)
            res = client.get('/api/v1/states/')
            self.assertEqual(res.status_code, 200)

    def test_get_state_id(self):
        """Test if it return the state by its id or not"""
        with app.test_client() as client:
            state = State(name="Finland")
            state.save()
            res = client.get('/api/v1/states/{}'.format(state.id))
            self.assertEqual(res.status_code, 200)

    def test_delete_states(self):
        """Test if it delete states by its ids or not"""
        with app.test_client() as client:
            state = State(name="Poland")
            state.save()
            res = client.get('/api/v1/states/{}'.format(state.id))
            self.assertEqual(res.status_code, 200)
            res2 = client.delete('/api/v1/states/{}'.format(state.id))
            self.assertEqual(res2.status_code, 200)
            res3 = client.get('/api/v1/states/{}'.format(state.id))
            self.assertEqual(res3.status_code, 404)

    def test_create_state(self):
        """Test if it create states or not"""
        with app.test_client() as client:
            res = client.post('/api/v1/states/',
                    data=json.dumps({"name": "Polands"}),
                    content_type="application/json")
            self.assertEqual(res.status_code, 201)

    def test_update_state(self):
        """Test if it update an user by its id or not"""
        with app.test_client() as client:
            state = State(name="Newland")
            state.save()
            res = client.put('/api/v1/states/{}'.format(state.id),
                    data=json.dumps({"name": "New York"}),
                    content_type="application/json")
            self.assertEqual(res.status_code, 200)


if __name__ == "__main__":
    unittest.main()
