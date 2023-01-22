#!/usr/bin/python3
"""
Flask route that returns json status response
"""
from api.v1.views import app_views
from flask import jsonify, request
from models import storage


@app_views.route('/status', methods=['GET'])
def status():
    """returns status"""
    if request.method == 'GET':
        status = {
            "status": "OK"
        }
        return (jsonify(status))


@app_views.route('/stats', methods=['GET'])
def stats():
    """retrieves the number of each objects by type"""

    given_models = {
        "User": "users",
        "Amenity": "amenities",
        "City": "cities",
        "Place": "places",
        "Review": "reviews",
        "State": "states",
    }

    response = {}

    for key, value in given_models.items():
        response[value] = storage.count(key)
        return jsonify(response)
