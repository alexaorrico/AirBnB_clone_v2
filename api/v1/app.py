#!/usr/bin/python3
"""This file defines the Flask application for the Airbnb clone API."""

from os import getenv
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS

app = Flask(__name__)

# Register blueprints
app.register_blueprint(app_views)
CORS(app, resources={"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_app(exception):
    """Handles teardown of the application context.

    Args:
        exception: An exception that occurred during request processing.
    """
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    '''
        Returns a JSON-formatted error response
    '''
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST", default="0.0.0.0")
    port = getenv("HBNB_API_PORT", default=5000)
    app.run(host, port, debug=True, threaded=True)
