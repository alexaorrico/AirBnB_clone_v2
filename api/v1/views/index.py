#!/usr/bin/python3
"""index file"""
from api.v1.views import app_views
from flask import jsonify, request
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """
    function for status route that returns the status
    """
    if request.method == 'GET':
        resp = {"status": "OK"}
        return jsonify(resp)

@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """
    an endpoint that retrieves the number of each objects by type
    """
    if request.method == 'GET':
        resp = {}
        sample = {"amenities": "Amenity",
                  "cities": "City",
                  "places": "Place",
                  "reviews": "Review",
                  "states": "State",
                  "users": "User"
        }
        for a, b in sample.items():
            resp[a] = storage.count(b)
        return jsonify(resp)
