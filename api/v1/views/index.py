#!/usr/bin/python3
""" returns json statuses for app_views routes  """
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def reoute_status():
    """first route
    Returns:
        json: json count number of instances
    """
    return jsonify({
        "status": "OK"
    }), 200


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def reoute_count():
    """endpoint of each objects by type"""
    count_stats = {
        'amenities': storage.count('Amenity'),
        'cities': storage.count('City'),
        'places': storage.count('Place'),
        'reviews': storage.count('Review'),
        'states': storage.count('State'),
        'users': storage.count('User')
    }
    return jsonify(count_stats)
