#!/usr/bin/python3
"""  the index.py file """
from flask import jsonify
from api.v1.views import app_views
from models import storage


# Define a route for /status on the app_views Blueprint
@app_views.route('/status', methods=['GET'], strict_slashes=False)
def get_status():
    """ the status"""
    return jsonify({"status": "OK"})


# Define a route for /stats on the app_views Blueprint
@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def get_stats():
    """ counts of each object type"""
    stats = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    return jsonify(stats)
