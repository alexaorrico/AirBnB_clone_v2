#!/usr/bin/python3
'''index file'''
from models import storage

from api.v1.views import app_views
from flask import jsonify, abort


@app_views.route('/status', strict_slashes=False)
def status():
    '''method to get status'''
    return jsonify({'status': 'OK'})


classes = {"amenities": 'Amenity', "cities": 'City', "places": 'Place',
           "reviews": 'Review', "states": 'State', "users": 'User'}


@app_views.route('/stats', strict_slashes=False)
def stat_count():
    '''count number of each objects by type'''
    resp = {}
    for key, value in classes.items():
        resp[key] = storage.count(value)
    if resp:
        return jsonify(resp)
    else:
        abort(404)
