#!/usr/bin/python3
'''testing the index route'''
import unittest
import pep8
from os import getenv
import requests
import json
from api.v1.app import *
from flask import request, jsonify
from models.user import User
from models import storage


class TestUsers(unittest.TestCase):
    '''test user'''
    def test_lists_users(self):
        '''test user GET route'''
        with app.test_client() as c:
            resp = c.get('/api/v1/users')
            self.assertEqual(resp.status_code, 200)
            resp2 = c.get('/api/v1/users/')
            self.assertEqual(resp.status_code, 200)

    def test_create_user(self):
        '''test user POST route'''
        with app.test_client() as c:
            resp = c.post('/api/v1/users/',
                          data=json.dumps(dict(email="123@abc.com",
                                               password="0000")),
                          content_type="application/json")
            self.assertEqual(resp.status_code, 201)

    def test_delete_user(self):
        '''test user DELETE route'''
        with app.test_client() as c:
            new_user = User(first_name="Mojo", last_name="Jojo",
                            email="123@abc.com", password="0000")
            storage.new(new_user)
            resp = c.get('api/v1/users/{}'.format(new_user.id))
            self.assertEqual(resp.status_code, 200)
            resp1 = c.delete('api/v1/users/{}'.format(new_user.id))
            self.assertEqual(resp1.status_code, 404)
            resp2 = c.get('api/v1/users/{}'.format(new_user.id))
            self.assertEqual(resp2.status_code, 404)

    def test_get_user(self):
        '''test user GET by id route'''
        with app.test_client() as c:
            new_user = User(first_name="Mojo", last_name="Jojo",
                            email="123@abc.com", password="0000")
            storage.new(new_user)
            resp = c.get('api/v1/users/{}'.format(new_user.id))
            self.assertEqual(resp.status_code, 200)

    def test_update_user(self):
        '''test user PUT route'''
        with app.test_client() as c:
            new_user = User(first_name="Mojo", last_name="Jojo",
                            email="123@abc.com", password="0000")
            storage.new(new_user)
            resp = c.put('api/v1/users/{}'.format(new_user.id),
                         data=json.dumps({"first_name": "Sailor",
                                          "last_name": "Moon"}),
                         content_type="application/json")
            # data = json.loads(resp.data.decode('utf-8'))
            # print(data)
            self.assertEqual(resp.status_code, 200)


if __name__ == '__main__':
    unittest.main()
