#!/usr/bin/python3
"""
Module contains status endpoint
"""

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status")
def get_status():
    """
    Endpoint to get API status
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def count():
    """
    Return the count of all the classes contained in models
    """
    total = {}
    classes = {
            "Amenity": "amenities",
            "City": "cities",
            "Place": "place",
            "Review": "reviews",
            "State": "states",
            "User": "users"
            }
    for cls in classes:
        count = storage.count(cls)
        total[classes.get(cls)] = count
    return jsonify(total)
