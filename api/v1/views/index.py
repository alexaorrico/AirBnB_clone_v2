#!/usr/bin/python3
"""Define API routes"""

from flask import jsonify
from api.v1.views import app_views
from models import storage

@app_views.route('/status', methods=['GET'])
def status():
    """Return the status of the API"""
    return jsonify({"status": "OK"})

@app_views.route('/stats', methods=['GET'])
def stats():
    """Return the number of each object by type"""
    classes = {
        "amenities": "Amenity",
        "cities": "City",
        "places": "Place",
        "reviews": "Review",
        "states": "State",
        "users": "User"
    }
    stats = {}
    for key, class_name in classes.items():
        count = storage.count(classes[class_name])
        stats[key] = count
    return jsonify(stats)
