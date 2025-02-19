#!/usr/bin/python3
"""
Index module to handle the API status route
"""
from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/stats', methods=['GET'])
def get_stats():
    """
    Retrieves the number of each object type
    """
    stats = {
        "amenities": storage.count('Amenity'),
        "cities": storage.count('City'),
        "places": storage.count('Place'),
        "reviews": storage.count('Review'),
        "states": storage.count('State'),
        "users": storage.count('User')
    }
    return jsonify(stats)
