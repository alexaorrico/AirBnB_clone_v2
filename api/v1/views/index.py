#!/usr/bin/python3
"""a blueprint module"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def status():
    """returns a json"""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def stats():
    """retrieves the number of each objects by type"""
    stats = {"amenities": 'Amenity',
             "cities": 'City',
             "places": 'Place',
             "reviews": 'Review',
             "states": 'State',
             "users": 'User'}
    for key in stats.keys():
        stats[key] = storage.count(stats.get(key))
    return jsonify(stats)
