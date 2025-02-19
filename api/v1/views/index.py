#!/usr/bin/python3
"""Index Module"""
from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route("/status")
def get_status():
    """Return a response status"""
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def get_stats():
    """Return a response status"""
    return jsonify({"amenities": storage.count("Amenity"),
                    "cities": storage.count("City"),
                    "places": storage.count("Place"),
                    "reviews": storage.count("Review"),
                    "states": storage.count("State"),
                    "users": storage.count("User")})
