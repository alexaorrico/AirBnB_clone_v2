#!/usr/bin/python3
"""Index file"""

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', strict_slashes=False)
def status():
    """Return status"""
    return ({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def stats():
    """Function that return stats"""
    classes = {
        "amenities": "Amenity",
        "cities": "City",
        "places": "Place",
        "reviews": "Review",
        "states": "State",
        "users": "User"
    }
    new_json = {}
    for key, value in classes.items():
        new_json[key] = storage.count(value)
    return jsonify(new_json)
