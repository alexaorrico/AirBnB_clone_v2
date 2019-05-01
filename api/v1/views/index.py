#!/usr/bin/python3
"""Defines a status route for the HolbertonBnB API."""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status")
def status():
    """Returns the server status.

    Returns:
        JSON object with the current server status.
    """
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def stats():
    """Retrives the count of each object type.

    Returns:
        JSON object with the number of objects by type."""
    return jsonify({
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    })
