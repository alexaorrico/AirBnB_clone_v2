#!/usr/bin/python3
"""
Flask route that returns json status response
"""
from flask import jsonify, request
from api.v1.views import app_views
from models import storage


@app_views.route('/status', methods=['GET'])
def status():
    """Returns the status"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def get_stats():
    """
    Retrieves the number of each object by type
    """
    stats = {
        "amenity": storage.count("Amenity"),
        "city": storage.count("City"),
        "place": storage.count("Place"),
        "review": storage.count("Review"),
        "state": storage.count("State"),
        "user": storage.count("User")
    }
    return jsonify(stats)
