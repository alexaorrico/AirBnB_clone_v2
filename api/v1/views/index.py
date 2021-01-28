#!/usr/bin/python3
"""
initialize the package
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def jsonok():
    """return JSON"""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def eDict():
    nDict = {"Amenity": "amenities", "City": "cities", "Place": "places",
             "Review": "reviews", "State": "states", "User": "users"}
    voidDict = {}

    for key, value in nDict.items():
        voidDict[value] = storage.count(key)

    return jsonify(voidDict)
