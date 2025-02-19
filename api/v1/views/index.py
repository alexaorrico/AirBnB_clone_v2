#!/usr/bin/python3
"""
Index file for API views
"""

from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Return a JSON status of the API"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """Return the number of each object type"""
    classes = {
        "amenities": "Amenity",
        "cities": "City",
        "places": "Place",
        "reviews": "Review",
        "states": "State",
        "users": "User"
    }
    # Create a dictionary with the count of each class
    stats = {key: storage.count(cls) for key, cls in classes.items()}
    return jsonify(stats)
