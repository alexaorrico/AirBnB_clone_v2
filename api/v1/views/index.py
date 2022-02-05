#!/usr/bin/python3
"""
Index for hbnb REST api
"""
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
def api_status():
    """returns status of the api"""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def api_stats():
    """
    Returns statistics for the api
    The count of every entity
    """
    stat_dict = {}
    for key, value in stat_dict.items():
        stat_dict[key] = storage.count(value)
    return jsonify(stat_dict)
