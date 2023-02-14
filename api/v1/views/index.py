#!/usr/bin/python3
"""
creates a flask route that returns a json
"""

from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status')
def status():
    ''' responds to /status route and returns status '''
    return (jsonify({'status': 'OK'}))


@app_views.route('/stats')
def stats():
    ''' responds to /stats route and returns number of objects by type '''
    ret = {
      "amenities": storage.count('Amenity'),
      "cities": storage.count('City'),
      "places": storage.count('Place'),
      "reviews": storage.count('Review'),
      "states": storage.count('State'),
      "users": storage.count('User')
    }
    return (jsonify(ret))
