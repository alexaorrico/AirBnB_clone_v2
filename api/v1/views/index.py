#!/usr/bin/python3
"""It creates a route /status on the object app_views"""
from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """It returns a JSON"""
    return jsonify({'status': 'OK'})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def endpoint():
    """It creates an endpoint"""
    return jsonify({"amenities": storage.count("Amenity"),
                    "places": storage.count("Place"),
                    "cities": storage.count("City"),
                    "reviews": storage.count("Review"),
                    "states": storage.count("State"),
                    "users": storage.count("User")
                    )}
