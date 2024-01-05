#!/usr/bin/python3
"""
This module defines routes for the API status and object counts.
"""

from flask import jsonify
from api.v1.views import app_views
from models import storage

# Create a route for /status on the app_views blueprint
@app_views.route('/status', methods=['GET'])
def get_status():
    status = {"status": "OK"}
    return jsonify(status)

# Create a route for /stats on the app_views blueprint
@app_views.route('/stats', methods=['GET'])
def get_stats():
    classes = {
        "Amenity": "amenities",
        "City": "cities",
        "Place": "places",
        "Review": "reviews",
        "State": "states",
        "User": "users"
    }

    stats = {class_name: storage.count(class_name) for class_name in classes}
    return jsonify(stats)
