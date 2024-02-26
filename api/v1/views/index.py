#!/usr/bin/python3
"""Status route for the AirBnB API"""
from flask import jsonify
from models import storage
from api.v1.views import app_views


@app_views.route("/status")
def status():
    """Returns the status of the server"""
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def stats():
    """Returns the number of each object type"""
    return jsonify({
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    })
