#!/usr/bin/python3
"""

"""
from api.v1.views import app_views
from flask import jsonify

from models import storage

classes = {
    "amenities": storage.count("Amenity"),
    "cities": storage.count("City"),
    "places": storage.count("Place"),
    "reviews": storage.count("Review"),
    "states": storage.count("State"),
    "users": storage.connt("User"),
}


@app_views.route("/status", methods=["GET"], strict_slashes=False)
def status_code():
    """
    status route
    """
    status = {"status": "OK"}
    return jsonify(status)


@app_views.route("/stats", methods=["GET"], strict_slashes=False)
def count_objects():
    respons = jsonify(classes)
    respons.status_code = 200
    return respons
