#!/usr/bin/python3
"""views index"""

from api.v1.views import app_views
from models import storage
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def stat():
    """return status code 200"""
    app_views = {'status': 'OK'}
    return jsonify(app_views), 200


@app_views.route('/stats', strict_slashes=False)
def stats():
    my_dict = {
        "amenities": storage.count('Amenity'),
        "cities": storage.count('City'),
        "places": storage.count('Place'),
        "reviews": storage.count('Review'),
        "states": storage.count('State'),
        "users": storage.count('User')
    }
    return jsonify(my_dict)
