#!/usr/bin/python3
"""Endpoint that retrieves the number of each objects by type"""
from api.v1.views import app_views
from flask import jsonify
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models.amenity import Amenity
import models


@app_views.route('/status', strict_slashes=False)
def status():
    """Returns status"""
    return (jsonify({"status": "OK"}))


@app_views.route('/stats', strict_slashes=False)
def stats():
    """Return stats"""
    my_dict = {
        "amenities": models.storage.count(Amenity),
        "cities": models.storage.count(City),
        "places": models.storage.count(Place),
        "reviews": models.storage.count(Review),
        "states": models.storage.count(State),
        "users": models.storage.count(User)
    }
    return my_dict
