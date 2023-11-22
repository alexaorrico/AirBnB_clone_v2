#!/usr/bin/python3
"""index script"""

from models import storage
from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status")
def status():
    """retrieve the status of the API"""
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def objects():
    """retrieve statistics on various objects"""
    return jsonify({
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    })
