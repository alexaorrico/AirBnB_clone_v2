#!/usr/bin/python3
"""index of routes for app_views"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', strict_slashes=False)
def status():
    """returns a JSON: "status": "OK" """
    return jsonify(status='OK')


@app_views.route('/stats', strict_slashes=False)
def stats():
    """retrieves number of each objects by type"""
    obj_stats = {
        'amenities': storage.count('Amenity'),
        'cities': storage.count('City'),
        'places': storage.count('Place'),
        'reviews': storage.count('Review'),
        'states': storage.count('State'),
        'users': storage.count('User'),
    }
    return jsonify(obj_stats)
