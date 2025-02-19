#!/usr/bin/python3
"""Index module"""

from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status', methods=['GET'])
def status():
    """Status route to return response in JSON"""
    data = {"status": "OK"}
    response = jsonify(data)

    return response


@app_views.route('/stats', methods=['GET'])
def stats():
    """Endpoint that retrieves the number of each objects by type"""
    data = {
        "amenities": storage.count('Amenity'),
        "cities": storage.count('City'),
        "places": storage.count('Place'),
        "reviews": storage.count('Review'),
        "states": storage.count('State'),
        "users": storage.count('User')
    }
    response = jsonify(data)

    return response
