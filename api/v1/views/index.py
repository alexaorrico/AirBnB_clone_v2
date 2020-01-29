#!/usr/bin/python3
"""status"""

from flask import jsonify, make_response
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


classes = {"amenities": Amenity,
           "cities": City,
           "places": Place,
           "reviews": Review,
           "states": State,
           "users": User}


@app_views.route("/status", strict_slashes=False)
def status():
    """status ok"""
    return make_response(jsonify({"status": "0K"}), 200)


@app_views.route("/stats", strict_slashes=False)
def stats():
    """count of objects by type"""
    adict = {}
    for key, value in classes.items():
        count = storage.count(value)
        adict[key] = count

    return jsonify(adict)
