#!/usr/bin/python3
"""Flask application that handle views"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def status_api():
    """Return the status 200"""
    return jsonify({'status': 'OK'})


@app_views.route('/stats')
def stats_api():
    """endpoint that retrieves the number of each objects by type"""
    return jsonify({
        'amenities': storage.count("Amenity"),
        'cities': storage.count("City"),
        'places': storage.count("Place"),
        'reviews': storage.count("Review"),
        'states': storage.count("State"),
        'users': storage.count("User")
    })
