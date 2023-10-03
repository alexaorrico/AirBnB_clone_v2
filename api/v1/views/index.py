#!/usr/bin/python3
"""
Flask application
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def status():
    """
    route for status
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def stats():
    """
    Returns the number of each instance type
    """
    return jsonify(amenities=storage.count("Amenity"),
                   cities=storage.count("City"),
                   places=storage.count("Place"),
                   reviews=storage.count("Review"),
                   states=storage.count("State"),
                   users=storage.count("User"))