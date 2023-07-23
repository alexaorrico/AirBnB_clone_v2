#!/usr/bin/python3
"""
Creates a route on the object app_views that returns a JSON
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', strict_slashes=False)
def status():
    """ Returns a JSON """
    return jsonify({'status': 'OK'})


@app_views.route('/stats', strict_slashes=False)
def show_stats():
    """Retrieves the number of each objects by type"""
    stats = {}
    stats['amenities'] = storage.count('Amenity')
    stats['cities'] = storage.count('City')
    stats['places'] = storage.count('Place')
    stats['reviews'] = storage.count('Review')
    stats['states'] = storage.count('State')
    stats['users'] = storage.count('User')
    return jsonify(stats)
