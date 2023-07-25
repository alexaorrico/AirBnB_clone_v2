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
        "Amenity": "amenities",
        "City": "cities",
        "Place": "places",
        "Review": "reviews",
        "State": "states",
        "User": "users"
    }
    return jsonify({k: storage.count(v) for k, v in classes.items()})
