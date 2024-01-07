#!/usr/bin/python3
"""
Flask API Route

This module defines a Flask route for the endpoint '/status'
The route returns a JSON response indicating the status as "OK"
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', methods=['GET'])
def display_status():
    """
    Route: /status

    Returns a JSON response indicating the status as "OK".

    Example:
    $ curl http://127.0.0.1:your_port/status
    Output: {"status": "OK"}
    """
    return jsonify({"status": "OK"})

@app_views.route('/api/v1/stats', methods=['GET'])
def show_data():
    """
    Retrieves the number of each objects by type.
    """
    stats = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    return jsonify(stats)
