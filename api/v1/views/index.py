#!/usr/bin/python3
""" Module for index.py """

from api.v1.views import app_views
from flask import jsonify
from models import storage

classes = {"amenities": "Amenity", "cities": "City", "places": "Place",
           "reviews": "Review", "states": "State", "users": "User"}


@app_views.route('/status', strict_slashes=False)
def get_status_route():
    """ Returns first json object """
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def get_obj_count_route():
    """ retrieves the number of each objects by type """
    count_dict = {}
    for k, v in classes.items():
        count_dict[k] = storage.count(v)
    return jsonify(count_dict)