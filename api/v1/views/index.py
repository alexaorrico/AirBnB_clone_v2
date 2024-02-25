#!/usr/bin/python3
""" app_view Blueprint """

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', strict_slashes=False)
def show_status():
    """ Shows the api response status """
    return jsonify(status="OK")


@app_views.route('/stats', strict_slashes=False)
def show_stats():
    """ Shows the number of each class objects """
    classes = {'amenities': 'Amenity', 'cities': 'City', 'places': 'Place',
               'reviews': 'Review', 'states': 'State', 'users': 'User'}
    class_count = {}
    for k, v in classes.items():
        class_count[k] = storage.count(v)
    return jsonify(class_count)
