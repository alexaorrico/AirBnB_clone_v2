#!/usr/bin/python3
""" Index file """
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status", methods=['GET'], strict_slashes=False)
def status():
    """ Status of API """
    return jsonify({"status": "OK"})


@app_views.route("/stats", methods=['GET'], strict_slashes=False)
def no_of_obj():
    """ retrieves the number of each object by type """
    names = ["amenities", "cities", "places", "reviews", "states", "users"]
    classes = ["Amenity", "City", "Place", "Review", "State", "User"]

    objs = {}
    for i in range(len(classes)):
        objs[names[i]] = storage.count(classes[i])

    return jsonify(objs)
