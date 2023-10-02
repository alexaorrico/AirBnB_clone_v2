#!/usr/bin/python3
"""
This module defines the routes for the API.
"""


from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage
app = Flask(__name__)


@app_views.route('/status')
def get_status():
    """
    Returns the status of the API.
    """
    return jsonify({"status": "OK"}), 200


@app_views.route('/api/v1/stats')
def get_stats():
    """
    Returns the number of each object by type.
    """
    obj_count = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    return jsonify(obj_count)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
