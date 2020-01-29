#!/usr/bin/python3
"""
    Module of blueprints of flask
"""
from models import storage
from flask import jsonify
from api.v1.views import app_views


@app_views.route("/status", strict_slashes=False)
def status_ok():
    """Send status of the application"""
    return jsonify({'status': 'OK'}), 200


@app_views.route("/stats", strict_slashes=False)
def fetch_all_stats():
    """Fetch of counts for all classes"""
    classes = {"amenities": "Amenity", "cities": "City", "places": "Place",
               "reviews": "Review", "states": "State", "users": "User"}
    count_dict = {}
    for key, value in classes.items():
        count = storage.count(value)
        count_dict[key] = count
    return jsonify(count_dict), 200
