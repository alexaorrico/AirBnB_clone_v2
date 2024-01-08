#!/usr/bin/python3
"""
module that is used for api index page
"""
from api.v1.views import app_views
from flask import jsonify, request
from models import storage


@app_views.route('/status', methods=['GET'])
def api_status():
    """ returns json string when request api status"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def returns_no():
        """Retrieves the number of each object type"""
    stats_dict = {
        'amenities': storage.count('Amenity'),
        'cities': storage.count('City'),
        'places': storage.count('Place'),
        'reviews': storage.count('Review'),
        'states': storage.count('State'),
        'users': storage.count('User')
    }
    return jsonify(stats_dict)
