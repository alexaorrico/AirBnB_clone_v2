#!/usr/bin/python3
"""Returns json status response"""
from api.v1.views import app_views
from flask import jsonify, request
from models import storage

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def stat():
    """Returns the status"""
    if request.method == 'GET':
        resp = {"status": "OK"}
        return jsonify(resp)

@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """Count of all class objects"""
    if request.method == 'GET':
        return jsonify(amenities=storage.count("Amenity"),
                   cities=storage.count("City"),
                   places=storage.count("Place"),
                   reviews=storage.count("Review"),
                   states=storage.count("State"),
                   users=storage.count("User"))
