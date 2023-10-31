#!/usr/bin/python3
"""
Status view for the AirBnB API.

This module defines a view for the status of the API.

Example:
    GET /api/v1/status:
    Returns a JSON response: {"status": "OK"}
"""

from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify
from models import storage


stats = {
    "amenities": "Amenity",
    "cities": "City",
    "places": "Place",
    "reviews": "Review",
    "states": "State",
    "users": "User"
}


@app_views.route('/status', strict_slashes=False)
def get_status():
    """
    Get the status of the API.

    Returns:
        JSON response containing the status.

    Example:
        {"status": "OK"}
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def get_stats():
    """
    Get the number of each object type.

    Returns:
        JSON response containing the count of each object type.
    """
    d_dict = {}
    for key, value in stats.items():
        d_dict[key] = storage.count(value)
    return jsonify(d_dict)


if __name__ == "__main__":
    pass
