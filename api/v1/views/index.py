#!/usr/bin/python3
"""
Flask route that returns json status response
"""
from api.v1.views import app_views
from flask import jsonify, request
from models import storage


@app_views.route('/status', methods=['GET'])
def status():
    """
    function for status route that returns the status
    """
    if request.method == 'GET':
        resp = {"status": "OK"}
        return jsonify(resp)


@app_views.route('/stats', strict_slashes=False)
def count():
    """Retrieves the number of each objects by type """
    cls_count = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
     }
    return jsonify(cls_count)


@app_views.route('/stats', methods=['GET'])
def stats():
    """
    function to return the count of all class objects
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
            response[value] = storage.count(key)
        return jsonify(response)
