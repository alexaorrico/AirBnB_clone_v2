#!/usr/bin/python3
from flask import Flask, render_template, abort, make_response, jsonify
from flask_cors import CORS
from models import storage
import os
from api.v1.views import app_views
import unittest
import pytest
import tempfile


@pytest.fixture
def client():
    test_db, flask.app.config['DATABASE'] = tempfile.mkstemp()
    flaskr.app.testing = True
    client = flask.app.test_client()

    with flask.app.app_context():
        flask.init_db()

    yield client

    os.close(test_db)
    os.unlink(flaskr.app.config['DATABASE'])

def test_status(self):
    response = client.get('/status')
    data = json.loads(response.get_data())
    print(data)
    self.assertEqual(response.status_code, 200)

def test_stats(self):
    response = client.get('/stats')
    data = json.loads(response.get_data())
    self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
