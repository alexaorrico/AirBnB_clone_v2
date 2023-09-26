#!/usr/bin/python3
"""
This module defines a Flask blueprint for handling status requests.
"""

from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User



@app_views.route("/status", methods=["GET"], strict_slashes=False)
def api_status():
    """a function to restore the state of the API"""
    return jsonify


@app_views.route("/stats", methods=["GET"], strict_slashes=False)
def obj_stats():
    """Rescue the numbers of each object by type"""
    classes = [Amenity, City, Place, Review, State, User]
    name = ["amenities", "cities", "places", "reviews", "states", "users"]

    num_objs = {}
    for i in range(len(classes)):
        num_objs[name[i]] = storage.count(classes[i])

    return jsonify(num_objs)
