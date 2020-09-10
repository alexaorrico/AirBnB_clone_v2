#!/usr/bin/python3
"""api.v1.views index"""
from api.v1.views import app_views
import models
from models import storage
from flask import jsonify


@app_views.route('/status')
def status():
    """ return ok """
    return {"status": "OK"}


@app_views.route('/stats')
def stats():
    """ return count of each object """
    dict = {
        "amenities": storage.count('Amenity'),
        "cities": storage.count('City'),
        "places": storage.count('Place'),
        "reviews": storage.count('Review'),
        "states": storage.count('State'),
        "users": storage.count('User')
    }
    return jsonify(dict)
