#!/usr/bin/python3
"""
Status of your API
"""

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def status():
    """
    Returns a JSON message
    """
    message = {"status": "OK"}
    return jsonify(message)


@app_views.route('/stats')
def stats():
    """
    Create an endpoint that retrieves the number of each objects by type
    """
    cls = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
        }
    return jsonify(cls)
