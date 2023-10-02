#!/usr/bin/python3
""" Routes of Flask app """

from api.v1.views import app_views
from flask import jsonify
from models import storage

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ Returns a status of Flask view """
    return jsonify({"status": "OK"})

@app_views.route('/api/v1/stats')
def stats():
    """ Returns a status of each object by type"""
    stats = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    return jsonify(stats)