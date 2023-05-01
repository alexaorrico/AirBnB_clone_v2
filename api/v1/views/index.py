#!/usr/bin/python3
"""
App views for AirBnB clone"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', methods=['GET'])
def status():
    """returns status"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def stats():
    """retrieves the number of each objects by type"""
    stats = {}
    classes = {"Amenity": "amenities",
               "City": "cities",
               "Place": "places",
               "Review": "reviews",
               "State": "states",
               "User": "users"}
    for cls in classes:
        count = storage.count(cls)
        stats[cls] = counts
    return jsonify(stats)
