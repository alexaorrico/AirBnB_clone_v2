#!/usr/bin/python3
"""
create a route /status on the object app_views
that returns a JSON: "status": "OK"
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def status():
    """return status in json format"""
    s = {"status": "OK"}
    return jsonify(s)


@app_views.route('/stats')
def stats():
    """retrieves the number of object """
    classes = {"amenities": "Amenity", "cities": "City",
               "places": "Place", "reviews": "Review",
               "states": "State", "users": "User"}
    retval = {}
    for key, val in classes.items():
        retval[key] = storage.count(val)
    return jsonify(retval)
