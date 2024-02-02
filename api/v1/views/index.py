#!/usr/bin/python3
"""
Flask route that returns json status response
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status", strict_slashes=False)
def status():
    """
    function for status route that returns the status
    """
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def stats():
    """
    Create an endpoint that retrieves the number of each objects by type
    """
    stats = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User"),
    }
    return jsonify(stats)
