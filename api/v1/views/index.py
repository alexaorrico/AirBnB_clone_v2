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
        "amenities": storage.count('amenities'),
        "cities": storage.count('cities'),
        "places": storage.count('places'),
        "reviews": storage.count('reviews'),
        "states": storage.count('states'),
        "users": storage.count('users')
    }
    return jsonify(js)
