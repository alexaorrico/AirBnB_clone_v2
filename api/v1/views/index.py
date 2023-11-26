#!/usr/bin/python3
"""
This script provides endpoints for the
application to check the status and stats.
"""

from api.v1.views import app_views
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage
from flask import jsonify


@app_views.route('/status')
def index():
    """
        Returns a JSON response indicating
        that the application is running.

        Returns: dict: A dictionary with a single
        key "status" and value "OK".
    """
    return jsonify({
       "status": "OK"
       })


@app_views.route('/stats')
def stats():
    """
    Returns a JSON response with the count of
    each type of object in the storage.

    Returns:
        dict: A dictionary with keys for each type of
        object and values for their counts.
    """
    classes = {
            "Amenity": Amenity, "City": City,
            "Place": Place, "Review": Review, "State": State, "User": User
            }
    c_lasses = {
            Amenity: "amenities", City: "cities",
            Place: "places", Review: "reviews", State: "states", User: "users"
            }
    obj_count = {}
    for item in classes:
        obj_type = classes[item]
        count = storage.count(obj_type)
        obj_count.update({c_lasses[obj_type]: count})
    return jsonify(obj_count)
