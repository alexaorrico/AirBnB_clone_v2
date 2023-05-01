#!/usr/bin/python3
"""
This module contains endpoint(route) status
"""
from models import storage
from flask import Flask
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def status():
    """
    Returns a JSON status
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def count():
    """
    Retrieves the number of each objects by type
    """
    return jsonify({"amenities": storage.count("Amenity"),
                    "cities": storage.count("City"),
                    "places": storage.count("Place"),
                    "reviews": storage.count("Review"),
                    "states": storage.count("State"),
                    "users": storage.count("User")})
