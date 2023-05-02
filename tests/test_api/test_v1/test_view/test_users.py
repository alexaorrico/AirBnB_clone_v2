#!/usr/bin/python3
"""
Testing users.py file
"""
from api.v1.app import (app)
import flask
import json
from models import storage
from models.user import User
import unittest


def getJson(response):
    """
    Extract the json dictionary from a flask Response object

    Argument:
        response: a reponse object from Flask

    Return:
        a dictionary or None or maybe raise an exception
    """
    return json.loads(str(response.get_data(), encoding="utf-8"))


class TestUserView(unittest.TestCase):
    """Test all routes in users.py"""

    @classmethod
    def setUpClass(cls):
        """set the flask app in testing mode"""
        app.config['TESTING'] = True
        cls.app = app.test_client()
        cls.path = "/api/v1"

    def test_getusers(self):
        """test listing all users"""
        user_args = {"first_name": "quokka", "email": "quokka@aww.com",
                     "password": "1234"}
        user = User(**user_args)
        user.save()
        rv = self.app.get('{}/users/'.format(self.path),
                          follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")
        json_format = getJson(rv)
        self.assertTrue(type(json_format), list)
        self.assertIn(user_args["first_name"], [e.get("first_name") for e
                                                in json_format])
        self.assertIn(user_args["email"], [e.get("email") for e
                                           in json_format])
        storage.delete(user)

    def test_view_one_user(self):
        """test retrieving one user"""
        user_args = {"first_name": "quokka", "id": "QO2",
                     "email": "quokka@aww.com", "password": "1234"}
        user = User(**user_args)
        user.save()
        rv = self.app.get('{}/users/{}'.format(
            self.path, user_args["id"]), follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")
        json_format = getJson(rv)
        self.assertEqual(json_format.get("first_name"),
                         user_args["first_name"])
        self.assertEqual(json_format.get("id"), user_args["id"])
        self.assertEqual(json_format.get("email"), user_args["email"])
        storage.delete(user)

    def test_view_one_user_wrong(self):
        """the id does not match a user"""
        user_args = {"first_name": "quokka", "id": "QO1",
                     "email": "quokka@aww.com", "password": "1234"}
        user = User(**user_args)
        user.save()
        rv = self.app.get('{}/users/{}'.format(self.path, "noID"),
                          follow_redirects=True)
        self.assertEqual(rv.status_code, 404)
        storage.delete(user)

    def test_delete_user(self):
        """test delete a user"""
        user_args = {"first_name": "quokka", "id": "QO",
                     "email": "quokka@aww.com", "password": "1234"}
        user = User(**user_args)
        user.save()
        rv = self.app.delete('{}/users/{}/'.format(
            self.path, user_args["id"]),
                                   follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")
        json_format = getJson(rv)
        self.assertEqual(json_format, {})
        self.assertIsNone(storage.get("User", user_args["id"]))

    def test_delete_user_wrong(self):
        """the id does not match a user"""
        user_args = {"first_name": "quokka", "id": "QO",
                     "email": "quokka@aww.com", "password": "1234"}
        user = User(**user_args)
        user.save()
        rv = self.app.delete('{}/users/{}/'.format(self.path, "noID"),
                             follow_redirects=True)
        self.assertEqual(rv.status_code, 404)
        storage.delete(user)

    def test_create_user(self):
        """test creating a user"""
        user_args = {"first_name": "quokka", "id": "QO",
                     "email": "quokka@aww.com", "password": "1234"}
        rv = self.app.post('{}/users/'.format(self.path),
                           content_type="application/json",
                           data=json.dumps(user_args),
                           follow_redirects=True)
        self.assertEqual(rv.status_code, 201)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")
        json_format = getJson(rv)
        self.assertEqual(json_format.get("first_name"),
                         user_args["first_name"])
        self.assertEqual(json_format.get("id"), user_args["id"])
        self.assertEqual(json_format.get("email"), user_args["email"])
        s = storage.get("User", user_args["id"])
        self.assertIsNotNone(s)
        storage.delete(s)

    def test_create_user_bad_json(self):
        """test creating a user with invalid json"""
        user_args = {"first_name": "quokka", "id": "QO",
                     "email": "quokka@aww.com", "password": "1234"}
        rv = self.app.post('{}/users/'.format(self.path),
                           content_type="application/json",
                           data=user_args,
                           follow_redirects=True)
        self.assertEqual(rv.status_code, 400)
        self.assertEqual(rv.get_data(), b"Not a JSON")

    def test_create_user_no_email(self):
        """test creating a user without email"""
        user_args = {"id": "ZA2",
                     "password": "1234"}
        rv = self.app.post('{}/users/'.format(self.path),
                           content_type="application/json",
                           data=json.dumps(user_args),
                           follow_redirects=True)
        self.assertEqual(rv.status_code, 400)
        self.assertEqual(rv.get_data(), b"Missing email")

    def test_create_user_no_pwd(self):
        """test creating a user without password"""
        user_args = {"id": "ZA2",
                     "email": "1234"}
        rv = self.app.post('{}/users/'.format(self.path),
                           content_type="application/json",
                           data=json.dumps(user_args),
                           follow_redirects=True)
        self.assertEqual(rv.status_code, 400)
        self.assertEqual(rv.get_data(), b"Missing password")

    def test_update_user_first_name(self):
        """test updating a user"""
        user_args = {"first_name": "quokka", "id": "QO1",
                     "email": "quokka@aww.com", "password": "1234"}
        user = User(**user_args)
        user.save()
        rv = self.app.put('{}/users/{}/'.format(self.path, user.id),
                          content_type="application/json",
                          data=json.dumps({"first_name": "Z"}),
                          follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")
        json_format = getJson(rv)
        self.assertEqual(json_format.get("first_name"), "Z")
        self.assertEqual(json_format.get("id"), user_args["id"])
        self.assertEqual(json_format.get("email"), user_args["email"])
        storage.delete(user)

    def test_update_user_id(self):
        """test cannot update user id"""
        user_args = {"first_name": "quokka", "id": "QO1",
                     "email": "quokka@aww.com", "password": "1234"}
        user = User(**user_args)
        user.save()
        rv = self.app.put('{}/users/{}/'.format(self.path, user.id),
                          content_type="application/json",
                          data=json.dumps({"id": "Z"}),
                          follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")
        json_format = getJson(rv)
        self.assertEqual(json_format.get("first_name"),
                         user_args["first_name"])
        self.assertEqual(json_format.get("id"), user_args["id"])
        self.assertEqual(json_format.get("email"), user_args["email"])
        storage.delete(user)

    def test_update_user_email(self):
        """test cannot update user email"""
        user_args = {"first_name": "quokka", "id": "QO1",
                     "email": "quokka@aww.com", "password": "1234"}
        user = User(**user_args)
        user.save()
        rv = self.app.put('{}/users/{}/'.format(self.path, user.id),
                          content_type="application/json",
                          data=json.dumps({"email": "Z@a.com"}),
                          follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")
        json_format = getJson(rv)
        self.assertEqual(json_format.get("first_name"),
                         user_args["first_name"])
        self.assertEqual(json_format.get("id"), user_args["id"])
        self.assertEqual(json_format.get("email"), user_args["email"])
        storage.delete(user)

    def test_update_user_bad_json(self):
        """test update with ill formed json"""
        user_args = {"first_name": "quokka", "id": "QO2",
                     "email": "quokka@aww.com", "password": "1234"}
        user = User(**user_args)
        user.save()
        rv = self.app.put('{}/users/{}/'.format(self.path, user.id),
                          content_type="application/json",
                          data={"id": "Z"},
                          follow_redirects=True)
        self.assertEqual(rv.status_code, 400)
        self.assertEqual(rv.get_data(), b"Not a JSON")
        storage.delete(user)

    def test_update_user_bad_id(self):
        """test update with no matching id"""
        user_args = {"first_name": "quokka", "id": "QO",
                     "email": "quokka@aww.com", "password": "1234"}
        user = User(**user_args)
        user.save()
        rv = self.app.put('{}/users/{}/'.format(self.path, "noID"),
                          content_type="application/json",
                          data=json.dumps({"id": "Z"}),
                          follow_redirects=True)
        self.assertEqual(rv.status_code, 404)
        storage.delete(user)


if __name__ == "__main__":
    unittest.main()
