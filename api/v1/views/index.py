#!/usr/bin/python3
""" Index for API"""
import models
from api.v1.views import app_views
from flask import jsonify
from models.amenity import Amenity
from models.city import City
from models.state import State
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route("/status", strict_slashes=False)
def status():
    """ Display the status of the API"""
    return jsonify({"status": "OK"})


@app_views.route("/stats", strict_slashes=False)
def stats():
    """Retrieves the number of each objects"""
    dict_obj = {}
    classes = [Amenity, City, Place, Review, State, User]
    names = ["amenities", "cities", "places", "reviews", "states", "users"]

    for i in range(len(classes)):
        dict_obj[names[i]] = models.storage.count(classes[i])

    return jsonify(dict_obj)
