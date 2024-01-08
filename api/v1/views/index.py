#!/usr/bin/python3
"""Main file to set up API endpoints"""

from flask import Flask, Blueprint, jsonify
from api.v1.views import app_views
from models import storage


hbnbText = {
    "cities": "City",
    "amenities": "Amenity",
    "states": "State",
    "users": "User"
    "places": "Place",
    "reviews": "Review",
}


@app_views.route('/status', strict_slashes=False)
def hbnbStatus():
    """hbnbStatus"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def hbnbStats():
    """hbnbStats"""
    return_dict = {}
    for key, value in hbnbText.items():
        return_dict[key] = storage.count(value)
    return jsonify(return_dict)


if __name__ == "__main__":
    pass
