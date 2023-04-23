#!/usr/bin/python3
"""Module for index endpoint of the views module of v1 of the RESTful API"""

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status/', strict_slashes=False)
def status():
    """Returns status: OK JSON"""
    return jsonify({"status": "OK"})


@app_views.route('/stats/', strict_slashes=False)
def stats():
    """Returns number of objects by type"""
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
