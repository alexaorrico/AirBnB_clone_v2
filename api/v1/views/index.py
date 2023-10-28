#!/usr/bin/python3
"""
returns json status response
"""

from api.v1.views import app_views
from flask import jsonify, request
from models import storage


@app_views.route("/status", methods=["GET"])
def status():
    """
    Returns a JSON: "status": "OK"
    """

    if request.method == "GET":
        response = {"status": "OK"}
        return jsonify(response)


@app_views.route("/stats", methods=["GET"])
def stats():
    """Retrieves the number of each objects by type"""
    if request.method == "GET":
        data = {
            "amenities": storage.count("Amenity"),
            "cities": storage.count("City"),
            "places": storage.count("Place"),
            "reviews": storage.count("Review"),
            "states": storage.count("State"),
            "users": storage.count("User"),
        }
    return jsonify(data)
