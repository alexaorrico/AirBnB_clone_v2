#!/usr/bin/python3
"""Index file for views module"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def status():
    """Status route of API v1"""
    status_data = {"status": "OK"}
    return jsonify(status_data)


@app_views.route('/stats')
def stats():
    """
    an endpoint that retrieves the number
    of each objects by type
    """
    status_value = {"amenities": storage.count("Amenity"),
                    "cities": storage.count("City"),
                    "places": storage.count("Place"),
                    "reviews": storage.count("Review"),
                    "states": storage.count("State"),
                    "users": storage.count("User")}
    return jsonify(status_value)
