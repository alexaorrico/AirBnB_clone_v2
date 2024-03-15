#!/usr/bin/python3
""" Temp """
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ Retrieve API Status """

    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """ Retrieve stats of objects, by class """

    classes = {
        'amenities': 'Amenity',
        'cities': 'City',
        'places': 'Place',
        'reviews': 'Review',
        'states': 'State',
        'users': 'User'
    }

    stats = {}
    for cls_name, cls in classes.items():
        count = storage.count(cls)
        stats[cls_name] = count
    return jsonify(stats)
