#!/usr/bin/python3
"""Defines the API routes for the Flask app"""

from api.v1.views import app_views
from models import storage
from flask import jsonify, Blueprint



@app_views.route('/stats', methods=['GET'])
def get_stats():
    """Returns the number of objects in the data store"""
    stats = {
        'amenities': storage.count('Amenity'),
        'cities': storage.count('City'),
        'places': storage.count('Place'),
        'reviews': storage.count('Review'),
        'states': storage.count('State'),
        'users': storage.count('User'),
    }
    return jsonify(stats)
