#!/usr/bin/python3

"""
this view manages default responses from the API

Author:
Khotso Selading and Londeka Dlamini
"""

from api.v1.views import app_views
from models import storage
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def status():
    """
    Returns a JSON status
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def stats():
    """
    Returns number of each JSON object created
    """
    return jsonify({"amenities": storage.count('Amenity'),
                    "cities": storage.count('City'),
                    "places": storage.count('Place'),
                    "reviews": storage.count('Review'),
                    "states": storage.count('State'),
                    "users": storage.count('User')
                    })
