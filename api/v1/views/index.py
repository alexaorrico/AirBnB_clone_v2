#!/usr/bin/python3
"""Routing functions"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def show_status():
    """Shows the status
           Returns:
               A JSON string of the status in a 200 response
    """
    return jsonify({'status': 'OK'})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def get_stats():
    """Gets stats for models
           Returns:
               A JSON representation of the number of each object
               in the body of a 200 response
    """
    stats_dict = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }

    return jsonify(stats_dict)
