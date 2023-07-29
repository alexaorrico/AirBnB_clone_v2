#!/usr/bin/python3
"""Flask with general routes"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status", methods=['GET'])
def status():
    """Returns a JSON status"""
    return jsonify({"status": "OK"})


@app_views.route("/stats", methods=['GET'])
def stats():
    """Retrieves the number of each objects by type"""
    classes = {
            "amenities": storage.count("Amenity"),
            "City": storage.count("City"),
            "Place": storage.count("Place"),
            "Review": storage.count("Review"),
            "State": storage.count("State"),
            "User": storage.count("User")
    }
    return jsonify(classes)
