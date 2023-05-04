#!/usr/bin/python3
"""import app_views from api.v1.views
create a route /status on the object app_views that returns a JSON: status:
    OK (see example)"""
from flask import Flask, Blueprint, jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status', strict_slashes=False)
def _status():
    """ return a JSON file with Status: OK """
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def stats():
    """Create an endpoint that retrieves the number of each objects by type"""
    countAmenity = storage.count("Amenity")
    countCities = storage.count("City")
    countPlaces = storage.count("Place")
    countReviews = storage.count("Review")
    countStates = storage.count("State")
    countUsers = storage.count("User")
    return jsonify(amenities=countAmenity,
                   cities=countCities,
                   places=countPlaces,
                   reviews=countReviews,
                   states=countStates,
                   users=countUsers)
