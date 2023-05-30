#!/usr/bin/python3
''' Index.py '''

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status")
def status():
    '''Checks status okay'''
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def stats():
    """retrieves the number of each objects by type"""
    objs = {"amenities": storage.count("Amenity"),
            "cities": storage.count("City"),
            "places": storage.count("Place"),
            "reviews": storage.count("Review"),
            "states": storage.count("State"),
            "users": storage.count("User")}
    return jsonify(objs)
