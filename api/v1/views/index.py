#!/usr/bin/python3
"""script to give status in JSON"""
from api.v1.views import app_views
from flask import request, jsonify
from models import storage


@app_views.route('/status', methods=['GET'])
def status_ok():
    """return JSON status ok"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def stats():
    """return the count of all objects"""
    response = {}
    instances = {
            "Amenity": "amenities",
            "City": "cities",
            "Place": "places",
            "Review": "reviews",
            "State": "states",
            "User": "users"
            }
    for key, value in instances.items():
        response[value] = storage.count(key)
    return jsonify(response)
