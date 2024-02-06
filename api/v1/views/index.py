#!/usr/bin/python3
""" implements various api routes"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status")
def status():
    """returns the status of api server"""
    api_status = {
        "status": "OK"
    }
    return jsonify(api_status)


@app_views.route("/stats")
def stats():
    """ method to give the statistics of all stored objects"""
    # mapping of classes to class name
    classes = {"amenities": "Amenity", "cities": "City", "places": "Place",
               "reviews": "Review", "states": "State", "users": "User"}
    statistics = {}

    for key, val in classes.items():
        statistics[key] = storage.count(val)

    return jsonify(statistics)
