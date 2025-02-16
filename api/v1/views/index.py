#!/usr/bin/python3
"""Index route for API"""
from flask import jsonify
from api.v1.views import app_views

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Returns the API status"""
    return jsonify({"status": "OK"})


"""Index route for API"""
from flask import jsonify
from api.v1.views import app_views
from models import storage

@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """Retrieve the number of each object by type"""
    stats = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    return jsonify(stats)
