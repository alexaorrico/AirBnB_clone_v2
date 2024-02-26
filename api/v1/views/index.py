#!/usr/bin/python3
"""index """
from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage


@app_views.route("/status")
def statue():
    """return the status"""
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def state_count():
    """return the count"""
    return jsonify(
        {
            "amenities": storage.count("amenity"),
            "cities": storage.count("city"),
            "places": storage.count("place"),
            "reviews": storage.count("review"),
            "states": storage.count("state"),
            "users": storage.count("user")
        }
    )
