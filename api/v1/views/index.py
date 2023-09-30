#!/usr/bin/python3
"""creates status"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


classes = {
    "amenities": "Amenity",
    "cities": "City",
    "places": "Place",
    "reviews": "Review",
    "states": "State",
    "users": "User"
}


@app_views.route('/status', strict_slashes=False)
def hbnb_status():
    """hbnb status"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def get_stats():
    """hbnb_stats"""
    obj_stats = {}
    for k, v in classes.items():
        obj_stats[k] = storage.count(v)
    return jsonify(obj_stats)
