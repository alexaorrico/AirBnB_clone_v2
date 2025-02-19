#!/usr/bin/python3
""" index """

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', methods=['GET'])
def get_status():
    """Returns the status of the API."""
    response = jsonify({"status": "OK"})
    response.headers['Content-Type'] = 'application/json'
    return response


@app_views.route("/stats", methods=['GET'], strict_slashes=False)
def stats():
    """stats route"""
    classes = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User"),
    }
    
    return jsonify(classes)
