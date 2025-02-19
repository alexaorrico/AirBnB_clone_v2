#!/usr/bin/python3
"""
This module defines API endpoints for checking ties: storage.count
Amenity the status of the service
and retrieving statistics about various objects in the storage.
"""

from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route("/status", methods=['GET'], strict_slashes=False)
def status():
    """
    Define a route for checking the status of the API
    :return: JSON response with status of the API

    """
    data = {
            "status": "OK"
            }
    response = jsonify(data)
    response.status_code = 200

    return response


@app_views.route("/stats", methods=['GET'], strict_slashes=False)
def stats():
    """
    Define a route for retrieving statistics of various objects in storage.
    :return: JSON response with the count of each object type

    """
    data = {
            "amenities": storage.count("Amenity"),
            "cities": storage.count("City"),
            "places": storage.count("Place"),
            "reviews": storage.count("Review"),
            "states": storage.count("State"),
            "users": storage.count("User"),
            }
    response = jsonify(data)
    response.status_code = 200

    return response
