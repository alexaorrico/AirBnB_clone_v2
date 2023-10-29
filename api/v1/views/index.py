#!/usr/bin/python3
""" index module """

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', methods=['GET'])
def status_json():
    """returns the status"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def get_number_of_objects_by_type():
    """Gets then number of objects per type and returns the stats"""
    stats = {
            "amenities": storage.count("Amenity"),
            "cities": storage.count("City"),
            "places": storage.count("Place"),
            "reviews": storage.count("Review"),
            "states": storage.count("State"),
            "users": storage.count("User")
            }
    return jsonify(stats)
