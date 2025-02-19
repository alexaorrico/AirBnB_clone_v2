#!/usr/bin/python3
""" Defines a status route """
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes = {"Amenity": Amenity, "City": City,
           "Place": Place, "Review": Review,
           "State": State, "User": User}


@app_views.route("/status", strict_slashes=False)
def status():
    """
    returns OK status
    """
    return jsonify({"status": "OK"})


@app_views.route("/stats", strict_slashes=False, methods=['GET'])
def stats():
    """
    returns counts of different objects
    """
    stats_dict = {}
    for obj in classes:
        stats_dict[obj] = storage.count(obj)
    return jsonify(stats_dict)
