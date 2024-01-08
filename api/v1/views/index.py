#!/usr/bin/python3
"""This module defines routes related to the status of the API"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from flask import Flask


@app_views.route('/status', strict_slashes=False)
def status():
    """Return JSON status response"""
    status = {"status": "OK"}
    return jsonify(status)


@app_views.route('/stats', strict_slashes=False)
def stats():
    """Return JSON stats response"""
    stats_data = {
            'amenities': storage.count('Amenity'),
            'cities': storage.count('City'),
            'places': storage.count('Place'),
            'reviews': storage.count('Review'),
            'states': storage.count('State'),
            'users': storage.count('User')
            }
    return jsonify(stats_data)
