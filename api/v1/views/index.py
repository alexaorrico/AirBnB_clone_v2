#!/usr/bin/python3
"""Index module"""
from . import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def status():
    """Status route to returns the status of the API"""
    return jsonify({'status': 'OK'})


@app_views.route('/stats')
def get_class_stat():
    """Retrieves the number of objects by type"""

    return jsonify({
        'amenities': storage.count("Amenity"),
        'cities': storage.count("City"),
        'places': storage.count("Place"),
        'reviews': storage.count("Review"),
        'states': storage.count("State"),
        'users': storage.count("User")
    })
