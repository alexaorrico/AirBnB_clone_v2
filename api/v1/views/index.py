#!/usr/bin/python3
"""
Module: index
"""
from api.v1.views import app_views, storage
from flask import jsonify


@app_views.route('/status/', strict_slashes=False)
def status():
    """ returns status: OK JSON  """
    return jsonify({"status": "OK"})


@app_views.route('/stats/', strict_slashes=False)
def stats():
    """ returns number of objects by type  """
    count_objects = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User"),
    }
    return jsonify(count_objects)
