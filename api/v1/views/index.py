#!/usr/bin/python3
""" index file for my flask application """

from api.v1.views import app_views
from flask import jsonify

my_classes = {"amenities": Amenity, "cities": City,
           "places": Place, "reviews": Review, "states": State, "users": User}

@app_views.route('/status/', strict_slashes=False)
def status():
    """return json object status"""
    return jsonify({"status": "OK"})

@app_views.route('/stats', strict_slashes=False)
def stats():
    """ retrieves the number of each objects by type """
    result = {}
    for item in classes:
        counts = storage.count(classes[item])
        result[item] = counts
    return jsonify(result)
