#!/usr/bin/python3
"""
import app_views from api.v1.views
create a route /status on the object app_views that returns
a JSON: "status": "OK" (see example)
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'])
def status():
    """status of API"""
    return jsonify({"status": "OK"})


@app_views.route('stats', methods=['GET'], strict_slashes=False)
def obj_num():
    """retrieves the number of each objects by type"""
    return jsonify({
        'amenities': storage.count('Amenity'),
        'cities': storage.count('City'),
        'places': storage.count('Place'),
        'reviews': storage.count('Review'),
        'states': storage.count('State'),
        'users': storage.count('User')
        })
