#!/usr/bin/python3
"""blueprint for app_views"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    '''returns the status of the server'''
    return jsonify({'status': 'OK'})

# task 4
@app_views.route('/stats', methods=['GET'])
def get_stats():
    """
    Retrieves the number of each objects by type
    """
    stats = {
            'amenites': storage.count('Amenity'),
            'cities': storage.count('City'),
            'places': storage.count('Place'),
            'reviews': storage.count('Review'),
            'states': storage.count('State'),
            'users': storage.count('User')

            }
    return jsonify(stats)
