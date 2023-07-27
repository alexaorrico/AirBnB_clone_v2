#!/usr/bin/python3
"""
Flask route that returns json status response
"""

from api.v1.views import app_views
from flask import jsonify, Blueprint
from models import storage


@app_views.route("/status", methods=["GET"], strict_slashes=False)
def status():
    """
    function for status route that returns the status
    """
    return jsonify({"status": "OK"})

@app_views.route('/stats', methods=['GET'])
def stats():
    amenities = storage.count("Amenity")
    cities = storage.count("City")
    places = storage.count("Place")
    reviews = storage.count("Review")
    states = storage.count("State")
    users = storage.count("User")

    stats = {
        "amenities": amenities,
        "cities": cities,
        "places": places,
        "reviews": reviews,
        "states": states,
        "users": users,
    }

    return jsonify(stats)
