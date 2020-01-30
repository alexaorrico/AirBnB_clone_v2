#!/usr/bin/python3
"""
Module for create route in the object and return a JSON status Ok
"""

from flask import jsonify
from api.v1.views import app_views
from models import storage

@app_views.route('/status')
def jsonReturn():
    """Return JSON"""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def statReturn():
    """Return Stats"""
    return jsonify({ "amenities": storage.count("Amenity"), 
                    "cities": storage.count("City"),
                    "places": storage.count("Place"),
                    "reviews": storage.count("Review"),
                    "states": storage.count("State"),
                    "users": storage.count("User")})
