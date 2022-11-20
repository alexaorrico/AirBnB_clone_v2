#!/usr/bin/python3

"""
This module contains some utility functions for the API
"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status_okay():
    """
    Returns Status OK code.
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def number_objects():
    """Returns number of objects by type"""
    classes = [Amenity, City, Place, Review, State, User]
    names = ["amenities", "cities", "places", "reviews", "states", "users"]

    number_objects = {}
    for i in range(len(classes)):
        number_objects[names[i]] = storage.count(classes[i])

    return jsonify(number_objects)
