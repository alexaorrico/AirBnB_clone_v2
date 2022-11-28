#!/usr/bin/python3
"""index fun stuff"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def status():
    """returns the status"""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def api_v1_stats():
    """returns the count of all objects"""
    return jsonify({
                    "amenities": storage.count("Amenity"),
                    "cities": storage.count("City"),
                    "places": storage.count("Place"),
                    "reviews": storage.count("Review"),
                    "states": storage.count("State"),
                    "users": storage.count("User")})
