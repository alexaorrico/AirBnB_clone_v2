#!/usr/bin/python3
"""
Create app view
"""

from flask import jsonify
from api.v1.views import app_views
from models import storage
from models import amenity, city, place, review, state, user


@app_views.route('/status', strict_slashes=False)
def status():
    ''' return status '''

    return (jsonify({"status": "OK"}))


@app_views.route('/stats', strict_slashes=False)
def stats():
    """Returns statistics."""

    # Get the counts from your data storage
    return jsonify({"amenities": storage.count("Amenity"),
                    "cities": storage.count("City"),
                    "places": storage.count("Place"),
                    "reviews": storage.count("Review"),
                    "states": storage.count("State"),
                    "users": storage.count("User")
                    })
