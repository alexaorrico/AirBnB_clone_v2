#!/usr/bin/python3
"""Flask route that returns json status response."""

from api.v1.views import app_views
from flask import jsonify, request
from models import storage


@app_views.route('/status', methods=['GET'])
def status():
    """mtd for status route, that returns the status."""
    if request.method == 'GET':
        resp = {"status": "OK"}
        return jsonify(resp)


@app_views.route('/stats', methods=['GET'])
def stats():
    """an endpoint that retrieves the number of each objects by type"""
    if request.method == 'GET':
        response = {}
        ITEMS = {
            "Amenity": "amenities",
            "City": "cities",
            "Place": "places",
            "Review": "reviews",
            "State": "states",
            "User": "users"
        }
        for key, value in ITEMS.items():
            response[value] = storage.count(key)
        return jsonify(response)
