#!/usr/bin/python3
"""Retrieve numnber of objects by type"""

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def statistics():
    """Retrieve number of each object by type"""
    return jsonify(
        {"amenities": storage.count("Amenity"),
         "cities": storage.count("City"),
         "places": storage.count("Place"),
         "reviews": storage.count("Review"),
         "states": storage.count("State"),
         "users": storage.count("User")})
