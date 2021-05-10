#!/usr/bin/python3
"""Retrieve status code"""
from flask import Flask, jsonify
from api.v1.views import app_views


@app_views.route('/status', strict_slashes=False)
def get_status():
    return jsonify({"status": "OK"})

@app_views.route("/stats", strict_slashes=False)
def stats():
    """Retrieves the number of each objects by type"""
    return jsonify({"amenities": storage.count("Amenity"),
                    "cities": storage.count("City"),
                    "places": storage.count("Place"),
                    "reviews": storage.count("Review"),
                    "states": storage.count("State"),
                    "users": storage.count("User")})
