#!/usr/bin/python3
"""
Index file
"""
from flask import jsonify
from api.v1.views import app_views
from models import storage
import models


@app_views.route('/status')
def Status():
    """Return object status"""
    status = {"status": "OK"}
    return jsonify(status)


@app_views.route('/stats')
def stats():
    """return count of categories"""
    stat_list = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User"),
    }
    return jsonify(stat_list)
