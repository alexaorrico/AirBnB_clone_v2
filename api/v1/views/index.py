#!/usr/bin/python3
"""
create a route /status on the object app_views that returns a JSON
and an endpoint that retrieves the number of each objects by type
"""

from flask import Flask, Blueprint, jsonify
from api.v1.views import app_views
from models import storage

@app_views.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "OK"})

@app_views.route('/status', methods=['GET'])
def get_stats():
    """function that returns the count of all class objects"""
     return_dict = {}
     hbnb = {
    "amenities": "Amenity",
    "cities": "City",
    "places": "Place",
    "reviews": "Review",
    "states": "State",
    "users": "User"
}
     for key, value in hbnb.items():
        return_dict[key] = storage.count(value)
    return jsonify(return_dict)
