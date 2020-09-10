#!/usr/bin/python3
"""Return the status of API"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'])
def status():
    """Returns the status of the API"""
    return jsonify({"status": "OK"}), 200


@app_views.route('/stats', strict_slashes=False, methods=['GET'])
def stats():
    """send json with the count of objects"""
    counts = {
        "amenities": storage.count('Amenity'),
        "cities": storage.count('City'),
        "places": storage.count('Place'),
        "reviews": storage.count('Review'),
        "states": storage.count('State'),
        "users": storage.count('User')
    }
    return jsonify(counts), 200
