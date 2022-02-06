#!/usr/bin/python3
"""index connects to API"""

from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify
from models import storage


hbnbText = {
    "amenities": "Amenity",
    "cities": "City",
    "places": "Place",
    "reviews": "Review",
    "states": "State",
    "users": "User"
}


@app_views.route('/status', strict_slashes=False)
def AppStatus():
    """hbnb status"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def AppStats():
    """hbnb stats"""
    new_dict = {}
    for key, value in hbnbText.items():
       new_dict[key] = storage.count(value)
    return jsonify(new_dict)

if __name__ == "__main__":
    pass
