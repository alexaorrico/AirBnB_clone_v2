#!/usr/bin/python3
""" a route /status on the object app_views that returns
    a JSON: "status": Ok
"""
from api.v1.views import app_views
from flask import jsonify
import json
from models import storage


@app_views.route('/status')
def status():
    """returns the url status"""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def stats():
    """returns number of each objects by type"""
    objs = {"amenities": 'Amenity', "cities": 'City', "places":
            'Place', "reviews": 'Review', "states": 'State', "users": 'User'}
    new_dict = {}
    for key, val in objs.items():
        new_dict[key] = storage.count(val)
    return jsonify(new_dict)
