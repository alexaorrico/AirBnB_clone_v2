#!/usr/bin/python3
"""returning status of the api"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status")
def status():
    """
    The function "status" returns a JSON object
    with the key "status" set to "ok".
    """
    arg = {
        "status": "OK"
          }
    return jsonify(**arg)


@app_views.route('/stats', methods=['GET'])
def get_stats():
    """Return /status api route"""
    stats = {
        'amenities': storage.count('Amenity'),
        'cities': storage.count('City'),
        'places': storage.count('Place'),
        'reviews': storage.count('Review'),
        'states': storage.count('State'),
        'users': storage.count('User')
    }
    return jsonify(**stats)
