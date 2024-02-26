#!/usr/bin/python3
"""A flask app"""

from flask import Flask, jsonify
import sys
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """Calls storage.close"""
    storage.close()


@app.errorhandler(404)
def error_handle(exception):
    """Handles the 404 error"""
    data = {"error": "Not found"}

    response = jsonify(data)
    return response


if __name__ == "__main__":
    app.run(getenv("HBNB_API_HOST"), getenv("HBNB_API_PORT"))
