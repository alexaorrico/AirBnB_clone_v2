#!/usr/bin/python3
"""create a route on the API"""

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', strict_slashes=False)
def status():
    """HBNB status"""
    text = {
        "status": "OK"
    }
    return jsonify(text)


@app_views.route('/stats', strict_slashes=False)
def stats():
    """HBNB stats for counting the number of objects"""
    classes = {"amenities": "Amenity", "cities": "City",
               "places": "Place", "reviews": "Review",
               "states": "State", "users": "User"}
    for key, value in classes.items():
        classes[key] = storage.count(value)
    return jsonify(classes)
