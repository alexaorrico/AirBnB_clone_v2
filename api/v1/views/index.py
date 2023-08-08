#!/usr/bin/python3
""" Module containing views """
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status", strict_slashes=False)
def status():
    """ returns a JSON """
    status = {"status": "OK"}
    return jsonify(status)


@app_views.route("/stats", strict_slashes=False)
def stats():
    """ retrieves the number of each objects by type """
    class_dict = {"Amenity": "amenities", "City": "cities", "Place": "places",
                  "Review": "reviews", "State": "states", "User": "users"}
    objs = {class_dict[cls]: storage.count(cls) for cls in class_dict}
    return jsonify(objs)
