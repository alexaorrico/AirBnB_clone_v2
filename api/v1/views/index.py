#!/usr/bin/python3
"""Index Module"""

from api.v1.views import app_views, State, City
from flask import Flask, jsonify

from models import storage


@app_views.route('/status', strict_slashes=False, methods=['GET'])
def status():
    """Return status OK"""
    return jsonify({"status": "OK"}), 200


@app_views.route('/stats', strict_slashes=False, methods=['GET'])
def stats():
    """Endpoint that retrieves the number of each object"""
    count = {
        "amenities": storage.count(State),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User)
    }
    return jsonify(count), 200
