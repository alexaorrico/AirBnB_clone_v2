#!/usr/bin/python3
"""
This module contains the index for the RESTful API
"""
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status')
def status():
    """Returns the status of the API"""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def stats():
    """Returns the stats of the API"""
    from models import storage
    classes = {
        "amenities": "Amenity",
        "cities": "City",
        "places": "Place",
        "reviews": "Review",
        "states": "State",
        "users": "User"
    }
    return jsonify({k: storage.count(v) for k, v in classes.items()})
