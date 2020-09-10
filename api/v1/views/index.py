#!/usr/bin/python3
"""This module is in charge of managing the index."""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models.amenity import Amenity


@app_views.route('/status')
def status():
    """Return the current status.

    Returns:
        dict: "OK"

    """
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def stats():
    """This method is responsible for returning the count of states.
    Returns:
        dict: returns the number of objects per state.
    """
    classes = {"amenities": storage.count(Amenity),
               "cities": storage.count(City),
               "places": storage.count(Place),
               "reviews": storage.count(Review),
               "states": storage.count(State),
               "users": storage.count(User)}
    return jsonify(classes)
