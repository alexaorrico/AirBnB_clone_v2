#!/usr/bin/python3
"""
Index module for handling the default route
"""

from api.v1.views import app_views, storage
from flask import jsonify


@app_views.route('/status/', strict_slashes=False)
def status():
    """Returns the status of the API"""
    return jsonify({"status": "OK"})


@app_views.route('/stats/', strict_slashes=False)
def stats():
    """Returns the count of each object by type"""
    class_counts = {}
    convert_dict = {
        'Amenity': 'amenities',
        'State': 'states',
        'City': 'cities',
        'User': 'users',
        'Place': 'places',
        'Review': 'reviews'
    }

    for _class in convert_dict.keys():
        class_counts[convert_dict[_class]] = storage.count(_class)

    return jsonify(class_counts)
