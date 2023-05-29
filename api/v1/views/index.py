#!/usr/bin/python3
"""an endpoint that retrieves the number of each objects by type"""

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status", strict_slashes=False)
def status():
    """Return the status"""
    return jsonify(status="OK")


@app_views.route("/api/v1/stats", strict_slashes=False)
def status():
    """Returns number of each type"""
    return jsonify(amenities=storage.count('Amenity'),
                   cities=storage.count('City'),
                   places=storage.count('Place'),
                   reviews=storage.count('Review'),
                   states=storage.count('State'),
                   users=storage.count('User')
                   )
