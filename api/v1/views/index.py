#!/usr/bin/python3
"""
Module contains status endpoint
"""

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status")
def get_status():
    """
    Endpoint to get API status
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def storage_count():
    """return the count of all the classes contained in models
    """
    cls_counts = {
            "amenities": storage.count("Amenity"),
            "cities": storage.count("City"),
            "places": storage.count("Place"),
            "reviews": storage.count("Review"),
            "states": storage.count("State"),
            "users": storage.count("Place")
            }
    return jsonify(cls_counts)
