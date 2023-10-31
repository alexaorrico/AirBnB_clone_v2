#!/usr/bin/python3
"""This module defines routes in the application"""

from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage


@app_views.route('status')
def return_status():
    """ returns a json response """
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def return_objects_by_type():
    """
    Retrieves the number of each objects by type
    """

    return jsonify({"amenities": storage.count("Amenity"),
                    "cities": storage.count("City"),
                    "places": storage.count("Place"),
                    "reviews": storage.count("Review"),
                    "states": storage.count("State"),
                    "users": storage.count("User")})
