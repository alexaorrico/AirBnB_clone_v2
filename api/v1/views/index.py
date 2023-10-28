#!/usr/bin/python3
"""index.py"""
from models import storage
from api.v1.views import app_views
from flask import jsonify
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route("/status", strict_slashes=False)
def status():
    """Returns status"""
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def stats():
    """counts and returns each table values"""
    classes = {"amenities": Amenity, "cities": City, "places": Place,
               "reviews": Review, "states": State, "users": User}
    stats_dict = {}
    for key, value in classes.items():
        stats_dict[key] = storage.count(value)
    return jsonify(stats_dict)
