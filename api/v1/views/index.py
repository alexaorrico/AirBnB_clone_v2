#!/usr/bin/python3
"""
This module defines a status route for the API.
"""

from api.v1.views import app_views
from flask import jsonify
from models import storage
import json


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """
    Returns the status of the API.
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """
    Retrieves the number of each object by type.
    """
    obj_count = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    response = json.dumps(obj_count, indent=2)
    response += '\n'  # Add a newline at the end
    return response, 200, {'Content-Type': 'application/json'}
