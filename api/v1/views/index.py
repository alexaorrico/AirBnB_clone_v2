#!/usr/bin/python3
"""Endpoint (route) will be to return the status of API"""
from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status', strict_slashes=False)
def status():
    """Returns a JSON of a string"""
    return jsonify({"status": "OK"})


@app_views.route('/stats',  strict_slashes=False)
def stats():
    """Creates an endpoint that retrieves the number of each objects by type"""
    return jsonify(
        amenities=storage.count(Amenity),
        cities=storage.count(City),
        places=storage.count(Place),
        reviews=storage.count(Review),
        states=storage.count(State),
        users=storage.count(User)
            )
