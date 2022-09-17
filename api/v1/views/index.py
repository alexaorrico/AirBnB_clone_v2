#!/usr/bin/python3
"""Module index"""
from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status', strict_slashes=False)
def status():
    """Returns a JSON"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def stats():
    """retrieves the number of each objects by type"""
    classes = {"User": "users", "Amenity": "amenities",
               "City": "cities", "Place": "places",
               "Review": "reviews", "State": "states"}
    new_dict = {}

    for i in classes.keys():
        stats[classes[cls]] = storage.count(cls)
    return jsonify(stats)