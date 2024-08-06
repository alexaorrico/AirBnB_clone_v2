#!/usr/bin/python3
"""Module to handle API routes related to object counts and status."""

from api.v1.views import app_views
from flask import jsonify
from models import storage

from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route("/status", strict_slashes=False)
def api_status():
    """Returns the status of the API."""
    return jsonify({"status": "OK"})


@app_views.route("/stats", strict_slashes=False)
def count_each_obj():
    """Retrieves the number of each object by type.

    Returns:
        JSON response with the count of each object type.
    """
    obj_counter = {
        "amenities": Amenity,
        "cities": City,
        "places": Place,
        "reviews": Review,
        "states": State,
        "users": User,
    }
    dic = {k: storage.count(v) for k, v in obj_counter.items()}

    return jsonify(dic)
