#!/usr/bin/python3
'''Index module for status'''
from flask import jsonify
from models import storage
from api.v1.views import app_views


@app_views.route('/status', strict_slashes=False)
def app_stat():
    '''display ok status'''
    return jsonify({'status': 'OK'})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def app_stats():
    '''retrieves the number of each objects by type'''
    stats = {
             "amenities": storage.count('Amenity'),
             "cities": storage.count('City'),
             "places": storage.count('Place'),
             "reviews": storage.count('Review'),
             "states": storage.count('State'),
             "users": storage.count('User')
            }
    return jsonify(stats)
