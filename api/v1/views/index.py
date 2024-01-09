#!/usr/bin/python3
"""
This module defines routes related to the status of the API
"""
from api.v1.views import app_views
from flask import Flask
from flask import jsonify
from models import storage


@app_views.route('/status', strict_slashes=False)
def status():
    """
    Return JSON status response
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def count():
    """
    Return JSON stats response
    """
    return jsonify({"amenities": storage.count("Amenity"),
                    "cities": storage.count("City"),
                    "places": storage.count("Place"),
                    "reviews": storage.count("Review"),
                    "states": storage.count("State"),
                    "users": storage.count("User")})
