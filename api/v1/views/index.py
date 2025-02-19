#!/usr/bin/python3
"""
index page
"""
from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route("/status", strict_slashes=False)
def get_status():
    """ Return status OK in json format for the Route"""
    return jsonify(status='OK')


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def get_stats():
    """number of each objects by type"""
    obj_dict = {
            "amenities": storage.count("Amenity"),
            "cities": storage.count("City"),
            "places": storage.count("Place"),
            "reviews": storage.count("Review"),
            "states": storage.count("State"),
            "users": storage.count("User")
        }
    return jsonify(obj_dict)
