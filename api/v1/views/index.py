#!/usr/bin/python3
"""Contains the index view for the API."""

from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status', methods=['GET'])
def api_status():
    """Return the status of the API."""
    response = {'status': 'OK'}
    return jsonify(response)


@app_views.route('/stats', methods=['GET'])
def get_stats():
    """Retrieves the number of objects for each type."""
    stats = {
        'amenities': storage.count('Amenity'),
        'places': storage.count('Place'),
        'cities': storage.count('City'),
        'reviews': storage.count('Review'),
        'states': storage.count('State'),
        'users': storage.count('User')
    }
    return jsonify(stats)
