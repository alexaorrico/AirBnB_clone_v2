#!/usr/bin/python3
"""List of states"""
from api.v1.views import app_views
from flask import jsonify, request
from models import storage


@app_views.route('/status')
def api_status():
    """api_status"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def stats():
    """
    returns the count of all the class objects.
    """
    if request.method == 'GET':

        response = {}

        PLURALS = {
            "Amenity": "amenities",
            "City": "cities",
            "Place": "places",
            "Review": "reviews",
            "State": "states",
            "User": "users"
        }

        for key, value in PLURALS.items():
            response[value] = len(storage.all(key))

        return jsonify(response)
