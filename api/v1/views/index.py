#!/usr/bin/python3
"""
Module that creates /status route on app_views object
Returns "status": "OK" JSON
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status", strict_slashes=False)
def status_route():
    """
    Returns "status": "OK"
    """
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def stats_route():
    """
    Retrieves the number of each objects by type
    """
    count_directory = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    return jsonify(count_directory)
