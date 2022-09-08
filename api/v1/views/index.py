#!/usr/bin/python3
"""
Status of your API
"""

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def status():
    message = {"status": "OK"}
    return jsonify(message)


@app_views.route('/stats')
def stats():
    cls = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
        }
    return jsonify(cls)
