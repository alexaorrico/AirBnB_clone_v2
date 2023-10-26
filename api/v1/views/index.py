#!/usr/bin/python3
"""
Status view for the AirBnB API.

This module defines a view for the status of the API.

Example:
    GET /api/v1/status:
    Returns a JSON response: {"status": "OK"}
"""

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', methods=['GET'])
def get_status():
    """
    Get the number of each object type.

    Returns:
        JSON response containing the count of each object type.
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
