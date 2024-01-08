#!/usr/bin/python3
"""flask  api views endpoint module"""
from models import storage
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status():
    """return json object"""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def stat_count():
    """Returns json object of
    each class"""
    return jsonify({'amenities': storage.count('Amenity')
                    'cities': storage.count('City'),
                    'places': storage.count('Place'),
                    'reviews': storage.count('Review'),
                    'states': storage.count('State'),
                    'users': storage.count('User')})
