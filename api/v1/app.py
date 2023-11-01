#!/usr/bin/python3
"""API status codes"""

from flask import Flask, jsonify
from .views import app_views
from . import models
from os import getenv
from flask_cors import CORS


app = Flask(__name__)

CORS(app, resources=r"/*", origins=["0.0.0.0"])

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(e=None):
    """Clean up the application context and exit."""
    models.storage.close()


@app.errorhandler(404)
def error(e):
    """Checks if the request is not found and returns a 404 error"""
    error = str(e).split()[0]
    output = e.description if "Not found" in e.description else "Not found"
    return jsonify({"error": output}), error


if __name__ == "__main__":
    app.run(getenv("HBNB_API_HOST"), getenv("HBNB_API_PORT"))
