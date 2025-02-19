#!/usr/bin/python3
"""
app.py

This module contains the main application logic.

It imports the necessary modules and classes, configures the Flask application,
and sets up the routes for the API endpoints.

Classes:
    None

Functions:
    None

Routes:
    None

Dependencies:
    - Flask
    - api.v1.views
    - models
    - models.amenity
    - models.city
    - models.place
    - models.review
    - models.state
    - models.user

"""

from os import getenv
from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={'/*': {'origins': '0.0.0.0'}})


@app.teardown_appcontext
def teardown(exc):
    """Function closes the storage"""
    storage.close()


@app.errorhandler(404)
def error_not_found(error):
    """Handles 404 errors, returns JSON-formatted stat code response"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', default='0.0.0.0')
    port = getenv('HBNB_API_PORT', default=5000)
    app.run(host=host, port=port, threaded=True)
