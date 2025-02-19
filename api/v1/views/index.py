#!/usr/bin/python3
"""
Creat Flask app; connect index.py to API
"""
from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage


@app_views.route('/status', strict_slashes=False)
def hbnb_status():
    """hbnb Status"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def hbnb_stats():
    """ Retrieves the number of each objects by type """
    hbnb_class = {
        "amenities": "Amenity",
        "cities": "City",
        "places": "Place",
        "reviews": "Review",
        "states": "State",
        "users": "User"
    }

    stats = {}
    for k, val in hbnb_class.items():
        stats[k] = storage.count(val)

    return jsonify(stats)
