#!/usr/bin/python3
import flask_unittest
from api.v1.app import app

class TestFoo(flask_unittest.ClientTestCase):
    # Assign the flask app object
    app = app(methods=['GET'])

    def test_foo_with_client(self, client):
        # Use the client here
        # Example request to a route returning "hello world" (on a hypothetical app)
        rv = client.get('/states')
        self.assertInResponse(rv, 'hello world!')
