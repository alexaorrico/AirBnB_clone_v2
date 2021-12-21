#!/usr/bin/python3
"""stats and status pages"""
from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage


@app_views.route('/status', strict_slashes=False)
def status():
    """status page"""
    return jsonify(status="OK")


@app_views.route('/stats', strict_slashes=False)
def get_stats():
    """shows number of each model"""
    return jsonify(amenities=storage.count("Amenity"),
                   cities=storage.count("City"),
                   places=storage.count("Place"),
                   reviews=storage.count("Review"),
                   states=storage.count("State"),
                   users=storage.count("User"))
