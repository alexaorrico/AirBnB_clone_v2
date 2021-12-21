#!/usr/bin/python3
"""Display the Index File"""

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def status():
    """Gets the Status of the page"""
    status = {"status": "OK"}
    return jsonify(status)


@app_views.route('/stats')
def stats():
    """Counts number of objects"""
    return jsonify({"amenities": storage.count("Amenity"),
                    "cities": storage.count("City"),
                    "places": storage.count("Place"),
                    "reviews": storage.count("Review"),
                    "states": storage.count("State"),
                    "users": storage.count("User")})
