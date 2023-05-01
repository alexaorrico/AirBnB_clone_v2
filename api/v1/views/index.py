#!/usr/bin/python3
""" index file for my flask application """

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status/', strict_slashes=False)
def status():
    """return json object status"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def stats():
    """ retrieves the number of each objects by type """
    my_dicts = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    return jsonify(my_dicts)
