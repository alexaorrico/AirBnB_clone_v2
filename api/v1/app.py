#!/usr/bin/python3

"""

This module creates and configures the Flask app, registers blueprints,
and sets up the teardown_appcontext to close the database connection.

"""

from flask import Flask, Blueprint, jsonify
from models import storage
import os
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(exception):
    """Close the storage"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Handles 404 errors and returns a JSON-formatted 404 response."""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(os.getenv("HBNB_API_PORT", 5000))
    app.run(host=host, port=port, threaded=True)
