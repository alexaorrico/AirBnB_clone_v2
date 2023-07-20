#!/usr/bin/python3
"""
app

This module contains the main Flask application for the API.
"""

from flask import Flask, jsonify
from flask_cors import CORS
from os import getenv

from api.v1.views import app_views
from models import storage


app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """
    teardown function

    This function is called when application context is torn down. It closes
    the database storage engine to free up resources.

    Args:
        exception (Exception): The exception that caused the teardown.
    """
    storage.close()


@app.errorhandler(404)
def handle_404(exception):
    """
    handles 404 error

    This function is called when a 404 error occurs. It returns a JSON response
    with an "error" key containing message "Not found" and status code of 404.

    Args:
        exception (Exception): The exception that caused the 404 error.

    Returns:
        Response: A JSON response with the error message and status code 404.
    """
    data = {
        "error": "Not found"
    }

    resp = jsonify(data)
    resp.status_code = 404

    return resp


if __name__ == "__main__":
    app.run(getenv("HBNB_API_HOST"), getenv("HBNB_API_PORT"))
