#!/usr/bin/python3
""" index file which returns json response on /status endpoint"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def get_status():
    """ returns json response to the route"""
    return jsonify(status="OK")


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def get_count():
    """returns number of each objects by type"""
    objects = {'amenities': 'Amenity', 'cities': 'City',
               'places': 'Place', 'reviews': 'Review',
               'states': 'State', 'users': 'User'}
    for key, value in objects.items():
        objects[key] = storage.count(value)
    return jsonify(objects)
