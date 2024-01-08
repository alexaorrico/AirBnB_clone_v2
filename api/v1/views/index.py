#!/usr/bin/python3
"""

This module defines the '/status' route that returns a JSON response.

"""

from api.v1.views import app_views
from flask import jsonify
import os
from models import storage


@app_views.route('/api/v1/stats', methods=['GET'], strict_slashes=False)
def get_stats():
    """Retrieves the number of each object type"""
    stats = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User"),
    }
    return jsonify(stats)
