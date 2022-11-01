#!/usr/bin/python3
"""
Flask route that returns json status response
"""

from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify, request
from models import storage

hbnbObjects = {
    "amenities": "Amenity",
    "cities": "City",
    "places": "Place",
    "reviews": "Review",
    "states": "State",
    "users": "User"
}


@app_views.route('/status', methods=['GET'])
def status():
    """
    function for status route that returns the status
    """
    if request.method == 'GET':
        resp = {"status": "OK"}
        return jsonify(resp)


@app_views.route('/stats', methods=['GET'])
def Stats():
    """an endpoint that retrieves the number of each objects by type
    """
    if request.method == 'GET':
        objCount_dict = {}
        for key, value in hbnbObjects.items():
            objCount_dict[key] = storage.count(value)
        return jsonify(objCount_dict)
