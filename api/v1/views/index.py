#!/usr/bin/python3
"""Index of app_views"""

from api.v1 import app_views
from flask import jsonify
from model import storage

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ Return status OK """
    return jsonify({"status": "OK"})

@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def get_stats():
    """ Retrieves the number of each object by type from /api/v1/stats """
    stats = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    
    return jsonify(stats)
