#!/usr/bin/python3
'''
routes:
/status
/stats
'''
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def status():
    """returns status: Ok"""
    return jsonify({'status': 'OK'})


@app_views.route('/stats')
def stats():
    """returns the number of instance"""
    stat = {
        'amenities': storage.count('Amenity'),
        'cities': storage.count('City'),
        'places': storage.count('Place'),
        'reviews': storage.count('Review'),
        'states': storage.count('State'),
        'users': storage.count('User')
    }
    return jsonify(stat)
