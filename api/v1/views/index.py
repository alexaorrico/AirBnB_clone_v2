#!/usr/bin/python3

from flask import Flask
from flask.globals import request
from flask.json import jsonify
from models import storage
from api.v1.views import app_views

data = {
    "amenities": "Amenity",
    "cities": "City",
    "places": "Place",
    "reviews": "Review",
    "states": "State",
    "users": "User"
}


@app_views.route('/status', strict_slashes=False)
def status():
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def Stats():
    """Create an endpoint that retrieves the number of each objects"""
    dict_data = {}
    for key, value in data.items():
        dict_data[key] = storage.count(value)
    return jsonify(dict_data)
