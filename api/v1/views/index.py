#!/usr/bin/python3
"""
import app_views,
create a route /status on the object
app_views that returns a JSON

"""

from flask import jsonify
from models import storage
from api.v1.views import app_views


@app_views.route('/status')
def status():
    """return status: OK"""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def stats():
    """returns count of models"""
    return jsonify(
        {
            "amenities": storage.count("Amenity"),
            "cities": storage.count("City"),
            "places": storage.count("Place"),
            "reviews": storage.count("Review"),
            "states": storage.count("State"),
            "users": storage.count("User")
        }
    )