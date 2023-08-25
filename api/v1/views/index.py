#!/usr/bin/python3
"""
    This module creates a status route for our blueprint
"""
from models import storage
from flask import jsonify
from api.v1.views import app_views


@app_views.route("/status", methods=["GET"])
def status():
    """get the status of the REST API"""
    return jsonify({"status": "OK"})


@app_views.route("/stats", methods=["GET"])
def get_instances():
    """get the number of instances of different objects"""
    from models.amenity import Amenity
    from models.city import City
    from models.place import Place
    from models.review import Review
    from models.state import State
    from models.user import User

    classes = {"amenities": Amenity, "cities": City,
               "places": Place, "reviews": Review,
               "states": State, "users": User
               }

    for key, value in classes.items():
        classes[key] = storage.count(value)

    return jsonify(classes)
