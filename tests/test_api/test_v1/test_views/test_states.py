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


class TestStates(unittest.TestCase):
    '''test state'''
    def test_lists_states(self):
        '''test state GET route'''
        with app.test_client() as c:
            resp = c.get('/api/v1/states')
            self.assertEqual(resp.status_code, 200)
            resp2 = c.get('/api/v1/states/')
            self.assertEqual(resp.status_code, 200)

    def test_create_state(self):
        '''test state POST route'''
        with app.test_client() as c:
            resp = c.post('/api/v1/states/',
                          data=json.dumps({"name": "California"}),
                          content_type="application/json")
            self.assertEqual(resp.status_code, 201)

    def test_delete_state(self):
        '''test state DELETE route'''
        with app.test_client() as c:
            new_state = State(name="Beckystan")
            storage.new(new_state)
            resp = c.get('api/v1/states/{}'.format(new_state.id))
            self.assertEqual(resp.status_code, 200)
            resp1 = c.delete('api/v1/states/{}'.format(new_state.id))
            self.assertEqual(resp1.status_code, 404)
            resp2 = c.get('api/v1/states/{}'.format(new_state.id))
            self.assertEqual(resp2.status_code, 404)

    def test_get_state(self):
        '''test state GET by id route'''
        with app.test_client() as c:
            new_state = State(name="Beckystan")
            storage.new(new_state)
            resp = c.get('api/v1/states/{}'.format(new_state.id))
            self.assertEqual(resp.status_code, 200)

    def test_update_state(self):
        '''test state PUT route'''
        with app.test_client() as c:
            new_state = State(name="Beckystan")
            storage.new(new_state)
            resp = c.put('api/v1/states/{}'.format(new_state.id),
                         data=json.dumps({"name": "Beckytopia"}),
                         content_type="application/json")
            # data = json.loads(resp.data.decode('utf-8'))
            # print(data)
            self.assertEqual(resp.status_code, 200)


if __name__ == '__main__':
    unittest.main()
