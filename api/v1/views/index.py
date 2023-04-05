#!/usr/bin/python3
"""Routes for app_views"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', strict_slashes=False)
def status():
    """Returns a JSON: "status": OK"""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def stats():
    """returns the count of all objects"""
    return jsonify({
                    "amenities": storage.count("Amenity"),
                    "cities": storage.count("City"),
                    "places": storage.count("Place"),
                    "reviews": storage.count("Review"),
                    "states": storage.count("State"),
                    "users": storage.count("User")})
