#!/usr/bin/python3
""" index file"""

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def view_json():
    """
    Return the current status in a JSON file form
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def stats():
    """
    Return the current status in a JSON file form
    """
    return jsonify({"amenities": storage.count("Amenity"),
                    "cities": storage.count("City"),
                    "places": storage.count("Place"),
                    "reviews": storage.count("Review"),
                    "states": storage.count("State"),
                    "users": storage.count("User")})
