#!/usr/bin/python3
"""file that return the status of the API"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', strict_slashes=False)
def status():
    """return the status of the API"""
    return (jsonify({"status": "OK"}))


@app_views.route('/stats', strict_slashes=False)
def count_objects():
    """ retrieves the number of each objects by type"""
    amenities = storage.count("Amentity")
    cities = storage.count("City")
    places = storage.count("Place")
    reviews = storage.count("Review")
    states = storage.count("State")
    users = storage.count("User")
    res = {"amenities": amenities,
           "cities": cities,
           "places": places,
           "reviews": reviews,
           "states": states,
           "users": users}
    return (jsonify(res))
