#!/usr/bin/python3
"""This module contains endpoint(route) status"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from flask import Flask


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """status of API"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
    """Retrieves the number of each objects by type"""
    return jsonify({"amenities": storage.count("Amenity"),
                    "cities": storage.count("City"),
                    "places": storage.count("Place"),
                    "reviews": storage.count("Review"),
                    "states": storage.count("State"),
                    "users": storage.count("User")})
