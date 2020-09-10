#!/usr/bin/python3
"""!!!!"""
from api.v1.views import app_views
from flask import Flask, jsonify, Blueprint
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


abnbText = {
    "amenities": "Amenity",
    "cities": "City",
    "places": "Place",
    "reviews": "Review",
    "states": "State",
    "users": "User"
}


@app_views.route('/status', strict_slashes=False)
def status():
    """status"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def hbnbStats():
    """Retrieve the stats"""
    new_dict = {}
    for key, value in abnbText.items():
        new_dict[key] = storage.count(value)
    return jsonify(new_dict)


if __name__ == "__main__":
    pass
