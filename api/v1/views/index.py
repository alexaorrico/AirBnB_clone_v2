#!/usr/bin/python3
"""flask with routes"""

from flask import jsonify
from . import app_views
from models import storage


@app_views.route('/status', strict_slashes=False)
def test_route():
    """tests route"""
    return jsonify({'status': 'OK'})


@app_views.route("/stats", strict_slashes=False)
def counts():
    """retrieves number of objects by type"""
    class_counts = {
            "amenities": storage.count("Amenity"),
            "cities": storage.count("City"),
            "places": storage.count("Place"),
            "reviews": storage.count("Review"),
            "states": storage.count("State"),
            "users": storage.count("User")
    }
    return jsonify(class_counts)
