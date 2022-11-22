#!/usr/bin/python3
"""
Module implements a rule that returns the status of application
"""

from flask import jsonify
import models
from api.v1.views import app_views
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status', strict_slashes=False)
def view_status():
    """
    Returns the status of API
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def view_stats():
    """
    Retrieves the number of each objects by type
    """
    return jsonify({
        "amenities": models.storage.count(Amenity),
        "cities": models.storage.count(City),
        "places": models.storage.count(Place),
        "reviews": models.storage.count(Review),
        "states": models.storage.count(State),
        "users": models.storage.count(User)
    })
