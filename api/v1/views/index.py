#!/usr/bin/python3
"""
This module contains the API route for the status of the API.

The API route for the status of the API is defined here.

Usage:
    The Blueprint app_views must be registered\
            with a Flask application instance
    to expose the API routes for version 1.\
            See api.v1.app for an example.
"""
from flask import jsonify
from api.v1.views import app_views
from models import storage,State,City,Amenity,User,Review


#api route status defination
@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """
    Returns the status of the API
    """
    return jsonify({"status": "OK"})

# api route  defination for the number objects
@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def get_stats():
    """
    Return the number of each object by type in the database.
    """
    objects = {
            "amenities": "Amenity",
            "cities": "City",
            "places": "Place",
            "reviews": "Review",
            "states": "State",
            "users": "User"
            }
    stats = {}
    for value in objects:
        stats[object[value]] = storage.count(value)
    return jsonify(stats)
