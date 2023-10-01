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
        "amenities": storage.count("amenities"),
        "cities": storage.count("cities"),
        "place": storage.count("place"),
        "reviews": storage.count("reviews"),
        "states": storage.count("states"),
        "users": storage.count("users")
    })
