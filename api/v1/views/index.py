#!/usr/bin/python3

"""index of the API connection"""
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
def status_api():
    """API status"""
    return jsonify({"status": "OK"})

@app_views.route("/stats", strict_slashes=False)
def show_stats():
    """show the count of object"""
    dict_stat = {}
    for key, value in hbnbText.items():
        dict_stat[key] = storage.count(value)
    return jsonify(dict_stat)

if __name__ == "__main__":
    pass
