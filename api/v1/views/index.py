#!/usr/bin/python3
""" This module uses blueprint to generate views
"""

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status", strict_slashes=False)
def status():
    """Return the status of the application"""
    text = {"status": "OK"}
    return jsonify(text)


@app_views.route("/stats", strict_slashes=False)
def stats():
    """Return the stats of the application"""
    classes = {
        "amenities": "Amenity",
        "cities": "City",
        "places": "Place",
        "reviews": "Review",
        "states": "State",
        "users": "User",
    }
    for key, value in classes.items():
        classes[key] = storage.count(value)
    return jsonify(classes)
