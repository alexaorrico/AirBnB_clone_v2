#!/usr/bin/python3
"""an object that returns a JSON: "status": "OK"""
from flask import jsonify
from models import storage
from api.v1.views import app_views

@app_views.route('/status', methods=['GET'])
def show_status():
    """returns the status"""
    if request.method == 'GET':
        response = {"status": "OK"}
        return jsonify(response)

@app_views.route('/stats', methods=['GET'])
def get_stats():
    """retrieves the number of each objects by type"""
    if request.method == 'GET':
        response = {}
        obj_plurals= {
            "Amenity": "amenities",
            "City": "cities",
            "Place": "places",
            "Review": "reviews",
            "State": "states",
            "User": "users"
        }
        for key, value in obj_plurals.items():
            response[value] = storage.count(key)
        return jsonify(response)
