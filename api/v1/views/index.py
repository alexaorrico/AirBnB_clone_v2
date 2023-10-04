#!/usr/bin/python3
""" Index """

from api.v1.views import app_views
from flask import jsonify
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage


@app_views.route("/status", methods=["GET"], strict_slashes=False)
def status():
    """
    Returns a JSON response with the status message "OK"
    """
    return jsonify({"status": "OK"})


class_dict = {
    "amenities": Amenity,
    "cities": City,
    "places": Place,
    "reviews": Review,
    "states": State,
    "users": User,
}


@app_views.route("/api/v1/stats", methods=["GET"], strict_slashes=False)
def stats():
    """
    Returns the number of objects in each class in the storage.

    :return: JSON response containing the number of objects for each class.
    """
    num_objs = {}
    for i in range(len(class_dict)):
        num_objs[class_dict.keys[i]] = storage.count(class_dict.values[i])

    return jsonify(num_objs)
