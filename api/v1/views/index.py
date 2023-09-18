#!/usr/bin/python3
"""import Blueprint from flask doc
create a variable app_views which is an instance of Blueprint
(url prefix must be /api/v1)
wildcard import of everything in the package api.v1.views.index => PEP8
will complain about it,
don’t worry, it’s normal and this file (v1/views/__init__.py)
won’t be check."""
from flask import jsonify
import models
from api.v1.views import app_views
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route("/status", strict_slashes=False)
def view_status():
    """View function  that returns a JSON: "status": OK """
    return jsonify({"status": "OK"})


@app_views.route("/stats", strict_slashes=False)
def view_stats():
    """Veiw function that retrieves the number of each object by type"""
    return jsonify({
        "amenities": models.storage.count(Amenity),
        "cities": models.storage.count(City),
        "places": models.storage.count(Place),
        "reviews": models.storage.count(Review),
        "states": models.storage.count(State),
        "users": models.storage.count(User)
    })
