#!/usr/bin/python3
"""
create a route /status on the object app_views
"""
from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route("/status", strict_slashes=False)
def status():
    '''returns a JSON: "status": "OK"'''
    return jsonify(status='OK')


@app_views.route("/stats", strict_slashes=False)
def stats():
    '''an endpoint that retrieves the number of each object"'''
    objects = {
            "amenities": "Amenity",
            "cities": "City",
            "places": "Place",
            "reviews": "Review",
            "states": "State",
            "users": "User"
            }
    itemcount = {}
    for key, value in objects.items():
        itemcount[key] = storage.count(value)

    return jsonify(itemcount)
