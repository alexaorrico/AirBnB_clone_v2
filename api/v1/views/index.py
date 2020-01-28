#!/usr/bin/python3
"""
Status of touy API
"""

from flask import jsonify
from api.v1.views import app_views
from models.state import State
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage


@app_views.route('/status', strict_slashes=False)
def app_view():
    """
    object app_view
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def count_objs():
    new_objs = {}
    objects = {"amenities": Amenity, "cities": City, "places": Place,
               "reviews": Review, "states": State, "users": User}
    for key, val in objects.items():
        new_objs[key] = storage.count(val)
    return jsonify(new_objs)
