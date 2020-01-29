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


@app_views.route("/status")
def status():
    """status ok"""
    return jsonify({"status": "0K"})


@app_views.route("/stats")
def stats():
    """count of objects by type"""
    adict = {}
    for key, value in classes.items():
        count = storage.count(value)
        adict[key] = count

    return jsonify(adict)
