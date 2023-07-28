#!/usr/bin/python3
"""
index.py
This module creates a route /status on the object app_views
that returns a JSON: "status": "OK"
"""

from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route("/status", methods=["GET"])
def show_status():
    """ returns a JSON that displays the status """
    return jsonify({"status": "OK"})


@app_views.route("/stats", methods=["GET"])
def show_stats():
    """ returns a JSON that displays the number of each object by type"""
    statistics = {"amenities": storage.count("Amenity"),
                  "cities": storage.count("City"),
                  "places": storage.count("Place"),
                  "reviews": storage.count("Review"),
                  "states": storage.count("State"),
                  "users": storage.count("User")}

    return jsonify(statistics)
