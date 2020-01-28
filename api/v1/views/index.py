#!/usr/bin/python3
"""
Module for status and stats endpoint
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status", methods=['GET'], strict_slashes=False)
def status():
    """
    create a route /status on the object app_views
    that returns a JSON: "status": "OK"
    """
    return jsonify(status='OK')


@app_views.route("/stats")
def stats():
    """
    Create an endpoint that retrieves the number of each objects by type.
    """
    return jsonify(amenities=storage.count('Amenity'),
                   cities=storage.count('City'),
                   places=storage.count('Place'),
                   reviews=storage.count('Review'),
                   states=storage.count('State'),
                   users=storage.count('User')
                   )
