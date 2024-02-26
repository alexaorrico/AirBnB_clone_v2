#!/usr/bin/python3
"""
Creates a routes on the object
"""

from api.v1.views import app_views
from flask import jsonify

from models import storage


# We define a route on app_view object
@app_views.route('/status', methods=['GET'])
def status():
    """ returns a JSON status """
    json_status = {
        "status": "OK"
    }
    return jsonify(json_status), 200


@app_views.route('/stats', methods=['GET'])
def stats():
    """
    Creates an endpoint that retrives number of objects by type
    """
    object_data = {
        "amenities": storage.count("Amenities"),
        "cities": storage.count("Cities"),
        "places": storage.count("Places"),
        "reviews": storage.count("Reviews"),
        "states": storage.count("States"),
        "users": storage.count("Users")
    }
    return jsonify(object_data), 200
