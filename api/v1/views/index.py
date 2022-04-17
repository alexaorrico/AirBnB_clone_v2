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
    func for status route
    """
    if request.method == 'GET':
        response = {"status": "OK"}
        return jsonify(response)

@app_views.route('/stats', methods=['GET'])
def stats():
    """
    Endpoint that retrieves the number of each objects by type
    """
    if request.method == 'GET':
        response = {}
        Entities = {
            "Amenity":"amenities",
            "City":"cities",
            "Place":"places",
            "Review":"reviews",
            "State":"states",
            "User":"users"
        }
        for key, value in Entities.items():
            response[value] = storage.count(key)
        return jsonify(response)
