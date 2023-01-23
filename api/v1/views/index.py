#!/usr/bin/python3
from api.v1.views import app_views
from models import storage
from flask import jsonify, request


@app_views.route('/status', methods=['GET'])
def response():
    """Status: Ok"""
    if request.method == 'GET':
        res = {"status": "Ok"}
        return jsonify(res)


@app_views.route('/stats', methods=['GET'])
def class_counter():
    """Get a dictionary from count method"""
    if request.method == 'GET':
        response = {}
        PLURALS = {
            "amenities": "Amenity",
            "cities": "City",
            "places": "Place",
            "reviews": "Review",
            "states": "State",
            "users": "User"
        }
        for key, value in PLURALS.items():
            response[value] = storage.count(key)
        return jsonify(response)
    