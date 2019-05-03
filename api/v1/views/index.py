#!/usr/bin/python3
"""Defines a status route for the HolbertonBnB API."""
from flask import jsonify
from flasgger import swag_from
from models import storage
from api.v1.views import app_views


@app_views.route("/status")
@swag_from("../apidocs/status/status.yml")
def status():
    """Returns the server status.

    Returns:
        JSON object with the current server status.
    """
    return jsonify({"status": "OK"})


@app_views.route("/stats")
@swag_from("../apidocs/stats/stats.yml")
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
