#!/usr/bin/python3
""" Create a Index """
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status")
def status():
    """Returns status in jason format"""
    return jsonify({'status': 'OK'})


@app_views.route("/stats")
def stats():
    """return count objects"""
    results = {}
    names = {"Amenity":  "amenities",
             "City":  "cities",
             "Place":  "places",
             "Review":  "reviews",
             "State":  "states",
             "User":  "users"}

    for key, value in sorted(names.items()):
        results[value] = storage.count(key)

    return jsonify(results)
