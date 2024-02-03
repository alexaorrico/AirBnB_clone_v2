#!/usr/bin/python3
"""
API V1 index views.
This module provides the HTTP methods for status and stats routes.
"""
from flask import jsonify
from api.v1.views import app_views
from models import storage

# Dictionary mapping class names to their respective types in storage.
OBJECT_DICT = {
    'amenities': 'Amenity',
    'cities': 'City',
    'places': 'Place',
    'reviews': 'Review',
    'states': 'State',
    'users': 'User'
}


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def get_status():
    """
    Returns a JSON response with the status of the API.
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def get_stats():
    """
    Retrieves the count of each object type from storage.
    Converts class names in OBJECT_DICT to actual classes using the globals() function.
    Returns a JSON with the count of each object type.
    """
    stats = {obj: storage.count(globals()[cls]) for obj, cls in OBJECT_DICT.items()}
    return jsonify(stats)
