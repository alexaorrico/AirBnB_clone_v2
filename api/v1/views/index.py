#!/usr/bin/python3
"""a module as an index"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route("/status", strict_slashes=False)
def status():
    """a function to return status OK when visit /status"""
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def statistics():
    """a function to retrieve the number of each objects by type"""
    stats = {}
    objects = {
        "amenities": Amenity,
        "cities": City,
        "places": Place,
        "reviews": Review,
        "states": State,
        "users": User,
    }
    for key, value in objects.items():
        stats[key] = storage.count(value)
    return jsonify(stats)
