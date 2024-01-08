#!/usr/bin/python3
"""index default view"""

from flask import jsonify
from api.v1.views import app_views
from models import storage

@app_views.route("/status", strict_slashes=False)
def get_status():
    """get api status"""
    return jsonify({"status": "OK"})


@app_views.route("/stats", strict_slashes=False)
def object_stats():
    """retrieves the number of each objects by type"""
    obj_count = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    return jsonify(obj_count)
