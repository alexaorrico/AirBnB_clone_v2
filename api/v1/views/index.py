#!/usr/bin/python3
"""
module index
"""

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', strict_slashes=False)
def status():
    """ return status """
    return jsonify(status='OK')


@app_views.route("/stats", methods=['GET'])
def count_stats():
    """retrieves number  of each objects by type"""
    count_stats = {
        'amenities': storage.count('Amenity'),
        'cities': storage.count('City'),
        'places': storage.count('Place'),
        'reviews': storage.count('Review'),
        'states': storage.count('State'),
        'users': storage.count('User')
    }
    return jsonify(count_stats)
