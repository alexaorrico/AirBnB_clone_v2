#!/usr/bin/python3
"""testing the index route"""
import unittest
import pep8
from os import getenv
import requests
import json
from api.v1.app import *
from flask import request, jsonify
from models.user import User
from models import storage

class TestUsersFunctions(unittest.TestCase):
    """Test the users class functions"""
    def test_get_all_user(self):
        """Test if it gets all users or not"""
        with app.test_client() as client:
            res = client.get('/api/v1/users')
            self.assertEqual(res.status_code, 200)
            res1 = client.get('/api/v1/users/')
            self.assertEqual(res.status_code, 200)

    def test_get_user_based_on_id(self):
        """Test if it gets the user by its id or not"""
        with app.test_client() as client:
            user = User(first_name="Jecoub", last_name="Hock",
                            email="123@abc.com", password="0000")
            user.save()
            res = client.get('api/v1/users/{}'.format(user.id))
            self.assertEqual(res.status_code, 200)

    def test_delete_user_object(self):
        """Test if it deletes the user by its id or not"""
        with app.test_client() as client:
            user = User(first_name="John", last_name="Afleck",
                            email="123@abc.com", password="0000")
            user.save()
            res = client.get('api/v1/users/{}'.format(user.id))
            self.assertEqual(res.status_code, 200)
            res2 = client.delete('api/v1/users/{}'.format(user.id))
            self.assertEqual(res2.status_code, 200)
            res3 = client.get('api/v1/users/{}'.format(user.id))
            self.assertEqual(res3.status_code, 404)

    def test_create_user_object(self):
        """Test if it creates new user or not"""
        with app.test_client() as client:
            res = client.post('/api/v1/users/',
                          data=json.dumps(dict(email="123@abc.com",
                                               password="0000")),
                          content_type="application/json")
            self.assertEqual(res.status_code, 201)

    def test_update_user(self):
        """Test if it updates the user info by its id or not"""
        with app.test_client() as client:
            user = User(first_name="John", last_name="Cena",
                            email="123@abc.com", password="0000")
            user.save()
            res = client.put('api/v1/users/{}'.format(user.id),
                         data=json.dumps({"first_name": "Mr.",
                                          "last_name": "Royal Rumble"}),
                         content_type="application/json")
            self.assertEqual(res.status_code, 200)


if __name__ == "__main__":
    unittest.main()
