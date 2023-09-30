#!/usr/bin/python3
"""api end point
"""

from flask import jsonify
from api.v1.views import app_views
from models import storage

classes = {
        "amenities": "Amenity",
        "cities": "City",
        "places": "Place",
        "reviews": "Review",
        "states": "State",
        "users": "User"
        }


@app_views.route('/status')
def status():
    """returns a json"""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def stats():
    """retrieves the number of each objects by type"""
    objs = {}

    for key, value in classes.items():
        count = storage.count(value)
        objs[key] = count
    return jsonify(objs)
