#!/usr/bin/python3
"""Defines the status route for our API"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def status():
    """Returns JSON response for status OK """
    return jsonify({'status': 'OK'})


@app_views.route('/stats')
def stats():
    """Returns stats of the number of each object by type"""
    return jsonify({
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    })
