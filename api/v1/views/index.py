#!/usr/bin/python3
"""index.py to connect to API"""
from api.v1.views import app_views
from models.state import State
from models.amenity import Amenity
from models.user import User
from models.city import City
from models.review import Review
from models.place import Place
from models import storage
from flask import Flask, Blueprint, jsonify

classes = {
    "states": State,
    "cities": City,
    "reviews": Review,
    "users": User,
    "amenities": Amenity,
    "places": Place
}

@app_views.route('/status', strict_slashes=False)
def hbnbStatus():
    """hbnbStatus"""
    return jsonify({"status": "OK"})

@app_views.route('stats', strict_slashes=False)
def hbnbStats():
    """Showing the states of all the values"""
    data = {}
    for key, val in classes.items():
        data[key] = storage.count(val)
    return jsonify(data)