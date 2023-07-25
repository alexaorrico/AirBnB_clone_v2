#!/usr/bin/python3
"""index.py to connect to API"""
from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify
from models import storage


@app_views.route('/status', strict_slashes=False)
def hbnbStatus():
    """hbnbStatus"""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def stats():
    """ Returns stats message in JSON
    """
    amens = storage.count("Amenity")
    cities = storage.count("City")
    places = storage.count("Place")
    reviews = storage.count("Review")
    states = storage.count("State")
    users = storage.count("User")

    return ({"amenities": amens,
             "cities": cities,
             "places": places,
             "reviews": reviews,
             "states": states,
             "users": users})


if __name__ == "__main__":
    pass
