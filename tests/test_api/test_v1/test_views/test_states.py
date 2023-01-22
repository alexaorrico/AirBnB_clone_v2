#!/usr/bin/python3
"""
Contains tests for views state routes
"""

import unittest

from api.v1.app import app
from models import storage
from models.state import State


class TestViewsState(unittest.TestCase):
    """Test Class for Views State routes
    """

    def setUp(self):
        """Sets up the flask app for testing"""
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()
        self.state_1 = State(name="Addis Ababa")
        self.state_2 = State(name="Harar")
        storage.new(self.state_1)
        storage.new(self.state_2)
        storage.save()

    def tearDown(self):
        """Removes the flask app context"""
        storage.delete(self.state_1)
        storage.delete(self.state_2)
        storage.save()
        self.ctx.pop()

    def test_states_endpoint(self):
        """Tests the /state endpoint returns list of states"""
        response = self.client.get("/api/v1/states")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        data = list(response.get_json())
        result = filter(lambda state: state["id"] == self.state_1.id, data)
        self.assertIsNotNone(next(result))

    def test_state_get_endpoint_returns_state(self):
        """Tests the get /state/id endpoint returns a valid state"""
        response = self.client.get("/api/v1/states/{}".format(self.state_1.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        self.assertEqual(response.get_json()["id"], self.state_1.id)

    def test_state_get_endpoint_returns_404(self):
        """Tests the get /state/id endpoint returns a 404"""
        response = self.client.get("/api/v1/states/abc")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content_type, "application/json")
        self.assertEqual(response.json["error"], "Not found")

    def test_state_delete_endpoint_deletes_state(self):
        """Tests the delete /state/id endpoint returns a valid state"""
        state_3 = State(name="Wakanda")
        state_3.save()

        response = self.client.delete("/api/v1/states/{}".format(state_3.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 0)

    def test_state_delete_endpoint_returns_404(self):
        """Tests the delete /state/id endpoint returns a 404"""
        response = self.client.delete("/api/v1/states/abc")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content_type, "application/json")
        self.assertEqual(response.json["error"], "Not found")

    def test_states_post_endpoint_saves_state(self):
        """Tests the post /states endpoint saves a state"""
        response = self.client.post("/api/v1/states/", json={"name": "Dire"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.content_type, "application/json")

        id = response.get_json().get("id", None)
        self.assertIsNotNone(id)
        storage.delete(storage.get(State, id))
        storage.save()

    def test_states_post_endpoint_returns_not_json(self):
        """Tests the post /states endpoint returns 400"""
        response = self.client.post("/api/v1/states/")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content_type, "application/json")
        self.assertEqual(response.json["error"], "Not a JSON")

    def test_states_post_endpoint_returns_missing_attr(self):
        """Tests the post /states endpoint returns 400"""
        response = self.client.post("/api/v1/states/", json={"key": "Dire"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content_type, "application/json")
        self.assertEqual(response.json["error"], "Missing name")

    def test_state_put_endpoint_updates_state(self):
        """Tests the put /state/id endpoint updates state"""
        response = self.client.put(
            "/api/v1/states/{}".format(self.state_1.id),
            json={"name": "Dire"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        self.assertEqual(response.get_json()["id"], self.state_1.id)
        self.assertEqual(response.get_json()["name"], "Dire")

    def test_state_put_endpoint_returns_404(self):
        """Tests the put /state/id endpoint returns a 404"""
        response = self.client.put(
            "/api/v1/states/{}".format("abc"),
            json={"name": "Dire"},
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content_type, "application/json")
        self.assertEqual(response.json["error"], "Not found")

    def test_states_post_endpoint_returns_not_json(self):
        """Tests the post /states endpoint returns 400"""
        response = self.client.put("/api/v1/states/{}".format(
            self.state_1.id), )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content_type, "application/json")
        self.assertEqual(response.json["error"], "Not a JSON")
