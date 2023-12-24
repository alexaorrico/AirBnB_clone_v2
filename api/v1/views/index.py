#!/usr/bin/python3
"""
    nose
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def statusRoute():
    """Status Route"""
    return jsonify({
        "status": "OK"
    })


@app_views.route('/stats')
def statsRoute():
    """Stats Route"""
    return jsonify({
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    })
