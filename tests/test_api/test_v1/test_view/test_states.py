#!/usr/bin/python3
"""
Testing states.py file
"""
from api.v1.app import (app)
import flask
import json
from models import storage
from models.state import State
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


class TestStateView(unittest.TestCase):
    """Test all routes in states.py"""

    @classmethod
    def setUpClass(cls):
        """set the flask app in testing mode"""
        app.config['TESTING'] = True
        cls.app = app.test_client()
        cls.path = "/api/v1"

    def test_getstates(self):
        """test listing all states"""
        state_args = {"name": "Zanzibar"}
        state = State(**state_args)
        state.save()
        rv = self.app.get('{}/states/'.format(self.path))
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")
        json_format = getJson(rv)
        self.assertTrue(type(json_format), list)
        self.assertIn(state_args["name"], [e.get("name") for e in json_format])
        storage.delete(state)

    def test_getstates_empty_db(self):
        """test listing all states in empty db"""
        s = storage.all("State").values()
        for e in s:
            storage.delete(e)
        rv = self.app.get('{}/states/'.format(self.path))
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")
        json_format = getJson(rv)
        self.assertTrue(type(json_format), list)
        self.assertEqual(json_format, [])

    def test_view_one_state(self):
        """test retrieving one state"""
        state_args = {"name": "Zanzibar", "id": "ZA3"}
        state = State(**state_args)
        state.save()
        rv = self.app.get('{}/states/{}/'.format(self.path, state_args["id"]))
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")
        json_format = getJson(rv)
        self.assertEqual(json_format.get("name"), state_args["name"])
        self.assertEqual(json_format.get("id"), state_args["id"])
        storage.delete(state)

    def test_view_one_state_wrong(self):
        """the id does not match a state"""
        state_args = {"name": "Zanzibar", "id": "ZA1"}
        state = State(**state_args)
        state.save()
        rv = self.app.get('{}/states/{}/'.format(self.path, "noID"))
        self.assertEqual(rv.status_code, 404)
        storage.delete(state)

    def test_delete_state(self):
        """test delete a state"""
        state_args = {"name": "Zanzibar", "id": "ZA"}
        state = State(**state_args)
        state.save()
        rv = self.app.delete('{}/states/{}/'.format(self.path,
                                                    state_args["id"]),
                             follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")
        json_format = getJson(rv)
        self.assertEqual(json_format, {})
        self.assertIsNone(storage.get("State", state_args["id"]))

    def test_delete_state_wrong(self):
        """the id does not match a state"""
        state_args = {"name": "Zanzibar", "id": "ZA1"}
        state = State(**state_args)
        state.save()
        rv = self.app.delete('{}/states/{}/'.format(self.path, "noID"),
                             follow_redirects=True)
        self.assertEqual(rv.status_code, 404)
        storage.delete(state)

    def test_create_state(self):
        """test creating a state"""
        state_args = {"name": "Zanzibar", "id": "ZA2"}
        rv = self.app.post('{}/states/'.format(self.path),
                           content_type="application/json",
                           data=json.dumps(state_args),
                           follow_redirects=True)
        self.assertEqual(rv.status_code, 201)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")
        json_format = getJson(rv)
        self.assertEqual(json_format.get("name"), state_args["name"])
        self.assertEqual(json_format.get("id"), state_args["id"])
        s = storage.get("State", state_args["id"])
        self.assertIsNotNone(s)
        storage.delete(s)

    def test_create_state_bad_json(self):
        """test creating a state with invalid json"""
        state_args = {"name": "Zanzibar", "id": "ZA2"}
        rv = self.app.post('{}/states/'.format(self.path),
                           content_type="application/json",
                           data=state_args,
                           follow_redirects=True)
        self.assertEqual(rv.status_code, 400)
        self.assertEqual(rv.get_data(), b"Not a JSON")
        rv = self.app.post('{}/states/'.format(self.path),
                           content_type="application/x-www-form-urlencoded",
                           data=state_args,
                           follow_redirects=True)
        self.assertEqual(rv.status_code, 400)

    def test_create_state_no_name(self):
        """test creating a state without a name"""
        state_args = {"id": "ZA2"}
        rv = self.app.post('{}/states/'.format(self.path),
                           content_type="application/json",
                           data=json.dumps(state_args),
                           follow_redirects=True)
        self.assertEqual(rv.status_code, 400)
        self.assertEqual(rv.get_data(), b"Missing name")

    def test_update_state_name(self):
        """test updating a state"""
        state_args = {"name": "Zanzibar", "id": "ZA"}
        state = State(**state_args)
        state.save()
        rv = self.app.put('{}/states/{}/'.format(self.path, state.id),
                          content_type="application/json",
                          data=json.dumps({"name": "Z"}),
                          follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")
        json_format = getJson(rv)
        self.assertEqual(json_format.get("name"), "Z")
        self.assertEqual(json_format.get("id"), state_args["id"])
        storage.delete(state)

    def test_update_state_id(self):
        """test cannot update state id"""
        state_args = {"name": "Zanzibar", "id": "ZA4"}
        state = State(**state_args)
        state.save()
        rv = self.app.put('{}/states/{}/'.format(self.path, state.id),
                          content_type="application/json",
                          data=json.dumps({"id": "Z"}),
                          follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(rv.headers.get("Content-Type"), "application/json")
        json_format = getJson(rv)
        self.assertEqual(json_format.get("name"), state_args["name"])
        self.assertEqual(json_format.get("id"), state_args["id"])
        storage.delete(state)

    def test_update_state_bad_json(self):
        """test update with ill formedt json"""
        state_args = {"name": "Zanzibar", "id": "ZA5"}
        state = State(**state_args)
        state.save()
        rv = self.app.put('{}/states/{}/'.format(self.path, state.id),
                          content_type="application/json",
                          data={"id": "Z"},
                          follow_redirects=True)
        self.assertEqual(rv.status_code, 400)
        self.assertEqual(rv.get_data(), b"Not a JSON")
        storage.delete(state)

    def test_update_state_bad_id(self):
        """test update with no matching id"""
        state_args = {"name": "Zanzibar", "id": "ZA6"}
        state = State(**state_args)
        state.save()
        rv = self.app.put('{}/states/{}/'.format(self.path, "noID"),
                          content_type="application/json",
                          data=json.dumps({"id": "Z"}),
                          follow_redirects=True)
        self.assertEqual(rv.status_code, 404)
        storage.delete(state)


if __name__ == "__main__":
    unittest.main()
