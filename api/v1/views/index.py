#!/usr/bin/python3
"""This module implement a rule that returns the status of the application"""
from flask import jsonify
from models import storage
from api.v1.views import app_views


@app_views.route("/status", strict_slashes=False)
def status():
    """View function that return a json message"""
    return jsonify({"status": "OK"})


@app_views.route("/stats", strict_slashes=False)
def stats():
    """function that retrieves the number of each object by type"""
    object_count = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User"),
    }
    return jsonify(object_count)
