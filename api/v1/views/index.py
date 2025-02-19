#!/usr/bin/python3
""" Blueprint Views
"""
from api.v1.views import app_views
from flask import jsonify, make_response
from models import storage


@app_views.route('/status')
def status():
    """ Returns status of request
    """
    return jsonify({'status': 'OK'})


@app_views.route('/stats')
def stats():
    """ Returns the number of items in storage
    """
    classes = ['Amenity', 'City', 'Place', 'Review', 'State', 'User']
    json_keys = ['amenities', 'cities', 'places', 'reviews', 'states', 'users']
    dictionary = {}
    for i, cls in enumerate(classes):
        dictionary[json_keys[i]] = storage.count(cls)
    return jsonify(dictionary)
