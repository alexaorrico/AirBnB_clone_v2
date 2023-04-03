#!/usr/bin/python3
"""Set up routes for apps"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from flask import jsonify


@app_views.route('/status')
def status():
    return jsonify({"status": "OK"})


@app_views.route('/api/v1stats', methods=['GET'])
def get_stats():
    stats = {
        'amenities': storage.count('Amenity'),
        'cities': storage.count('City'),
        'places': storage.count('Place'),
        'reviews': storage.count('Review'),
        'states': storage.count('State'),
        'users': storage.count('User')
    }
    return jsonify(stats)
