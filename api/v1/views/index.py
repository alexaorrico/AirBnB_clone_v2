#!/usr/bin/python3
"""This is the endpoint (route) status"""
from models import storage
from flask import Flask
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def get_status():
    """Route to return a JSON status"""
    return jsonify({"status": "OK"})


@app_views.route('stats', strict_slashes=False)
def stats():
    """Retrieves objects by their type"""
    count = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
        }

    return jsonify(count)
