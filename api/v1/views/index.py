#!/usr/bin/python3
"""
index
"""
from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status', strict_slashes=False)
def status():
    """return status json"""
    return jsonify(status="OK")


@app_views.route('/stats', strict_slashes=False)
def stats():
    """that retrieves the number of each objects by type:"""
    classes = {"amenities": "Amenity", "cities": "City",
               "places": "Place",
               "reviews": "Review", "states": "State",
               "users": "User"}

    ct = {}
    for cls, value in classes.items():
        ct[cls] = storage.count(classes[cls])
    return jsonify(ct)
