#!/usr/bin/python3
"""
Flask route that returns json status response
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status", strict_slashes=False)
def status():
    """an endpoint that returns the status of the API"""
    return jsonify({"status": "OK"})


@app_views.route("/stats", methods=["GET"], strict_slashes=False)
def stats():
    """an endpoint that retrieves the number of each objects by type"""
    return jsonify(
        amenities=storage.count('Amenity'),
        cities=storage.count('City'),
        places=storage.count('Place'),
        reviews=storage.count('Review'),
        states=storage.count('State'),
        users=storage.count('User')
    )
