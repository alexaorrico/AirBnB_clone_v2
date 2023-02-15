#!/usr/bin/python3
"""
This module defines a Flask route /status and returns a JSON.
"""

from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route("/status", methods=["GET"])
def status():
    """
    Return a JSON with "status": "OK"
    """
    return jsonify({"status": "OK"})

@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def get_stats():
    """Retrieves the number of each objects by type"""
    classes = {
        "Amenity": "amenities",
        "City": "cities",
        "Place": "places",
        "Review": "reviews",
        "State": "states",
        "User": "users"
    }
    count_dict = {}
    for cls in classes:
        count_dict[classes[cls]] = storage.count(cls)
    return jsonify(count_dict)
