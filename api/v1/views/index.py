#!/usr/bin/python3
""" module"""

from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage


@app_views.route('/status', strict_slashes=False)
def status():
    """DOC"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def status_count():
    """Doc"""
    clss = {
        "Amenity": "amenities",
        "Place": "places",
        "State": "states",
        "Review": "reviews",
        "User": "users"
        "City": "cities",
        }
    d = {}
    for k, val in clss.items():
        d[val] = storage.count(k)
    return jsonify(d)
