#!/usr/bin/ python3
"""
Creates a status route
"""


from flask import jsonify
from api.v1 import views

from models import storage
import models

my_app = views.app_views


@my_app.route('/status', strict_slashes=False)
def getStatus():
    """returns the status of the API."""

    return jsonify({'status': 'OK'})


@my_app.route('/stats', strict_slashes=False)
def numObj():
    """returns the number of each object by type."""
    return jsonify({"amenities": storage.count("Amenity"),
                    "cities": storage.count("City"),
                    "places": storage.count("Place"),
                    "reviews": storage.count("Review"),
                    "states": storage.count("State"),
                    "users": storage.count("User")})
