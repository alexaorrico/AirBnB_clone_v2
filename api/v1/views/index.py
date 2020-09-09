#!/usr/bin/python3
"""Index file using blueprint"""
from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage


classes = {
    "amenities": "Amenity",
    "cities": "City",
    "places": "Place",
    "reviews": "Review",
    "states": "State",
    "users": "User"
    }


@app_views.route('/status', strict_slashes=False)
def index():
    """return a status"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def stats():
    """return a stats"""
    new_dict = {}
    for key, value in classes.items():
        new_dict[key] = storage.count(value)
    return jsonify(new_dict)


if __name__ == "__main__":
    pass
