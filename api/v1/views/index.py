#!/usr/bin/python3
"""Response Hanlders."""
from api.v1.views import app_views
from flask import jsonify, request
from models import storage


@app_views.route("/status", methods=["GET"])
def status():
    """Return 'OK' status."""
    if request.method == "GET":
        return jsonify({"status": "OK"})


@app_views.route("/stats", methods=["GET"])
def stats():
    """Return the global status."""
    if request.method == "GET":
        return jsonify(
            {
                "amenities": storage.count("Amenity"),
                "cities": storage.count("City"),
                "places": storage.count("Place"),
                "reviews": storage.count("Review"),
                "states": storage.count("State"),
                "users": storage.count("User"),
            }
        )
