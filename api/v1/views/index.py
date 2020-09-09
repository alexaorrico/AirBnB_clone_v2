#!/usr/bin/python3
"""!"""
from api.v1.views import app_views
from flask import Flask, jsonify, Blueprint
from models import storage


@app_views.route('/status', strict_slashes=False)
def status():
    return jsonify({"status": "OK"})

abnbText = {
    "amenities": "Amenity",
    "cities": "City",
    "places": "Place",
    "reviews": "Review",
    "states": "State",
    "users": "User"
}


@app_views.route('/stats', strict_slashes=False)
def hbnbStats():
    """Retrieve the stats"""
    new_dict = {}
    for key, value in abnbText.items():
        new_dict[key] = storage.count(value)
    return jsonify(new_dict)


if __name__ == "__main__":
    pass
