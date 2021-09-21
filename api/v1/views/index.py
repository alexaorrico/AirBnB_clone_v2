#!/usr/bin/python3
""" Index file for views """

from flask import jsonify
from models import storage
from api.v1.views import app_views


@app_views.route('/status')
def status():
    """Status"""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def stats():
    """
    endpoint that retrieves the number of each objects by type
    """
    counters = {"amenities": storage.count("Amenity"),
                "cities": storage.count("City"),
                "places": storage.count("Place"),
                "reviews": storage.count("Review"),
                "states": storage.count("State"),
                "users": storage.count("User")}
    return jsonify(counters)
