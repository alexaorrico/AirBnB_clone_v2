#!/usr/bin/python3
"""index page status"""

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status", strict_slashes=False)
def status():
    return jsonify({"status": "OK"})


@app_views.route("/stats", strict_slashes=False)
def stats():
    """ returns a count of all objects in storage """
    models = {
            "amenities": "Amenity", "cities": "City",
            "places": "Place", "reviews": "Review",
            "states": "State", "users": "User"
            }
    count = {}
    for k, v in models.items():
        count[k] = storage.count(v)
    return jsonify(count)
