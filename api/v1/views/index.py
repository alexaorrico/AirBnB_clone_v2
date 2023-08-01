#!/usr/bin/python3
"""index --connect to API"""
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


@app_views.route('/status')
def hbnbStatus():
    """hbnbStatus"""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def hbnbStats():
    """hbnbStats"""
    return_dict = {}
    for key, value in hbnbText.items():
        return_dict[key] = storage.count(value)
    return jsonify(return_dict)

if __name__ == "__main__":
    pass
