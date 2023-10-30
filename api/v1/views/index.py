#!/usr/bin/python3
"""
api/v1/views/index.py
Defines routes for the /status and /stats endpoints.
"""
from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status', methods=['GET'])
def status():
    """
    Endpoint to retrieve the API status.
    """
    return jsonify(status="OK")


@app_views.route('/stats', methods=['GET'])
def stats():
    """
    Endpoint to retrieve the number of objects by type.
    """
    stats_dict = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    return jsonify(stats_dict)
