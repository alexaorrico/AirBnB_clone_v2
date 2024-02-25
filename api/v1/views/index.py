#!/usr/bin/python3
"""Contains routes of the app"""
from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route("/status", methods=['GET'], strict_slashes=False)
def status():
    """status route
    Return: JSON representation of the response"""
    data = {
            "status": "OK"
           }
    response = jsonify(data)
    response.status_code = 200
    return response


@app_views.route("/stats", methods=['GET'], strict_slashes=False)
def stats():
    """endpoint that retrieves the number of each objects by type"""
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
