#!/usr/bin/python3
"""Load the json responses for the api"""
from api.v1.views import app_views
from flask import jsonify
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage


@app_views.route("/status")
def return_json():
    return jsonify(status="OK")


@app_views.route("/stats")
def get_stats():
    # Create an empty dict to be returned as json
    stat_dict = {}
    # Create a list of all the objects
    all_objects = {
                    "amenities": Amenity,
                    "cities": City,
                    "places": Place,
                    "reviews": Review,
                    "states": State,
                    "users": User
                  }
    # Loop through the list and carry out a count for each item
    for key, value in all_objects.items():
        stat_dict[key] = storage.count(value)
    # Return the JSONified version
    return jsonify(stat_dict)
