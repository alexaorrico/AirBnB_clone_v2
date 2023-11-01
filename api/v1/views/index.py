#!/usr/bin/python3
"""
This module imports the app view blueprint and defines
all associated methods with the blueprint
"""
from api.v1.views import app_views
from flask import jsonify
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage


@app_views.route("/status")
def api_ok():
    """
    This function simply determines if server
    serving api's is up and running
    """
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def number_per_object():
    """
    return the total number of objects
    per class
    """
    number_per_object = {
            "amenities": storage.count(Amenity),
            "cities": storage.count(City),
            "places": storage.count(Place),
            "reviews": storage.count(Review),
            "states": storage.count(State),
            "users": storage.count(User)
            }
    return jsonify(number_per_object)
