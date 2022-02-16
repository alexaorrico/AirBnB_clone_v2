#!/usr/bin/python3
""" This a index file"""

from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage

classes = {"Amenity": "amenities", "City": "cities", "Place": "places",
           "Review": "reviews", "State": "states", "User": "users"}


@app_views.route('/status', strict_slashes=False)
def status():
    """ Method that returns the status """
    return ({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def stats():
    """ Valid method of objects """
    num_obj = {}
    for key, value in classes.items():
        num_obj[value] = storage.count(key)
    return jsonify(num_obj)
