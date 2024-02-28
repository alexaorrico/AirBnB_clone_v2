#!/usr/bin/python3
"""
Module contains views (route) for status
"""
from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage


app = Flask(__name__)


@app_views.route('/status', strict_slashes=False)
def status():
    """Endpoint to check the status of the API"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def count():
    """
    retrieves the number of each objects by type"""
    return jsonify({"amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State")
        "users": storage.count("User")})
