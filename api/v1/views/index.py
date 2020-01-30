#!/usr/bin/python3
""" index file """

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def status():
    """ status function """
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def stats():
    """number of of objects by type"""
    dic = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        'places': storage.count('Place'),
        'reviews': storage.count('Review'),
        'states': storage.count('State'),
        'users': storage.count('User')
    }
    return jsonify(dic)
