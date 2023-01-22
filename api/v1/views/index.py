#!/usr/bin/python3
'''Defines the JSON GET request from the application'''
from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify
from models import storage


hbnbStats = {
    "amenities": "Amenity",
    "cities": "City",
    "places": "Place",
    "reviews": "Review",
    "states": "State",
    "users": "User"
}


@app_views.route("/status", strict_slashes=False)
def status():
    '''Returns JSON status'''
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def stats():
    '''Returns the number of each object by type'''
    dictionary = {}
    for key, value in hbnbStats.items():
        dictionary[key] = storage.count(value)
    return jsonify(dictionary)


if __name__ == "__main__":
    pass
