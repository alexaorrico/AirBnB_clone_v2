#!/usr/bin/python3
"""
Flask route that returns json
"""

from api.v1.views import app_views
from flask import jsonify, request
from models import storage


@app_views.route('/status', methods=['GET'])
def status():
    """
    function for returning status of the route
    """
    resp = {"status": "OK"}
    return jsonify(resp)


@app_views.route('/stats', methods=['GET'])
def stats():
    """
    return the count of all objects in the tables
    """
    objects = {
        "Amenity": "amenities",
        "Place": "places",
        "City": "cities",
        "Review": "reviews",
        "State": "states",
        "User": "users"
    }
    response = {}
    for key, value in objects.items():
        response[value] = storage.count(key)
    return jsonify(response)
