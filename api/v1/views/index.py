#!/usr/bin/python3
"""
Create a flask app that will serve the API, views module
"""
from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status')
def status():
    """
    Return status
    """
    response = {"status": "OK"}
    return jsonify(response)


@app_views.route('/stats')
def stats():
    """
    Return stats
    """
    response = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    return jsonify(response)
