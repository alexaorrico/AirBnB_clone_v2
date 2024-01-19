#!/usr/bin/python3
"""
    Main application module for the API.
    This module initializes the Flask application, registers blueprints,
    defines custom error handlers, and starts the development server.
"""


import os
from flask import Flask
from flask import jsonify
from models import storage
from api.v1.views import app_views


app = Flask(__name__)


app.register_blueprint(app_views, url_prefix="/api/v1")


@app.teardown_appcontext
def teardown_appcontext(exception):
    """
        Closes the storage on teardown.
    """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """
        Handles 404 errors and returns a JSON-formatted response.
    """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = os.environ.get('HBNB_API_HOST', '0.0.0.0')
    port = int(os.environ.get('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
