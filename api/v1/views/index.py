#!/usr/bin/python3
"""
File that configures the routes of index
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status")
def status():
    """
    Return the state of status
    """
    return jsonify(status="OK")


@app_views.route("/stats")
def stats():
    """
    Return the number of instances for each class
    """
    objects = {
        "Amenity": "amenities",
        "City": "cities",
        "Place": "places",
        "Review": "reviews",
        "State": "states",
        "User": "users"
        }

    obj_count = {}

    for key, val in objects.items():
        obj_count[val] = storage.count(key)

    return jsonify(obj_count)
