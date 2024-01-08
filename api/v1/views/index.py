#!/usr/bin/python3
"""flask  api views endpoint module"""
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
    return jsonify({'amenities': storage.count('Amenities'),
                    'cities': storage.count('Cities'),
                    'places': storage.count('Places'),
                    'reviews': storage.count('Reviews'),
                    'states': storage.count('States'),
                    'users': storage.count('Users')})
