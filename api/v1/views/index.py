#!/usr/bin/python3
"""
an endpoint that retrieves the number of each objects by type
"""
from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Return a JSON response indicating the status is 'OK'."""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def get_stats():
    """Retrieve the number of objects by type and return as JSON."""
    objects = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "user": storage.count("User")
    }
    return jsonify(objects)
