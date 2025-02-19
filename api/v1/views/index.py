#!/usr/bin/python3
""" Root API endpoints """

from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status')
def status():
    """ Returns the status of the API """
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def stats():
    """ Retrieves the number of each object by type """
    from models import storage
    stats = {
        'amenities': storage.count('Amenity'),
        'cities': storage.count('City'),
        'places': storage.count('Place'),
        'reviews': storage.count('Review'),
        'states': storage.count('State'),
        'users': storage.count('User')
    }
    return jsonify(stats)
