#!/usr/bin/python3
"""Module for connecting to the API"""

# Import statements
from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify
from models import storage


hbnb_text = {
    "amenities": "Amenity",
    "cities": "City",
    "places": "Place",
    "reviews": "Review",
    "states": "State",
    "users": "User"
}


@app_views.route('/status', strict_slashes=False)
def hbnb_status():
    """hbnbStatus"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def hbnb_stats():
    """hbnbStats"""
    return_dict = {}
    for key, value in hbnb_text.items():
        return_dict[key] = storage.count(value)
    return jsonify(return_dict)


if __name__ == "__main__":
    pass
