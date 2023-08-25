#!/usr/bin/python3
"""
Index
"""
from api.v1.views import app_views
from flask import jsonify, request
from models import storage


@app_views.route('/status', methods=['GET'])
def status():
    """
    Returns:
        Status of API
    """
    if request.method == 'GET'
        response = {"status": "OK"}
        return jsonify(response)


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def number_objs():
    """
    Endpoint
    """
    response = {}
    NAME = {
        "Amenity": "amenities",
        "City": "cities",
        "Place": "places",
        "Review": "reviews",
        "State": "states",
        "User": "users"
    }
    for key, value in NAME.items():
        response[value] = storage.count(key)
    return jsonify(response)