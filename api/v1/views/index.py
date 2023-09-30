#!/usr/bin/python3
"""
    module index
"""

from api.v1.views import app_views
from flask import Flask, jsonify

import models
from models import storage


@app_views.route('/status', methods=['GET'])
def statCode():
    """
        a function that return a json string containing
        the status code of the site
    """
    js = {'status': 'OK'}
    return jsonify(js)


@app_views.route('/api/v1/stats', methods=['GET'])
def objStats():
    """
        a function that retrieves the number of each objects by type
    """
    js = {
        "amenities": storage.count('Amenity'),
        "cities": storage.count('City'),
        "places": storage.count('Place'),
        "reviews": storage.count('Review'),
        "states": storage.count('State'),
        "users": storage.count('User')
    }
    return jsonify(js)
