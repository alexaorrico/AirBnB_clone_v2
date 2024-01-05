#!/usr/bin/python3
"""index"""


from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def status():
    """return status"""
    stat = {"status": "OK"}
# json_response_stat = jsonify(stat)
    return jsonify(stat), 200


@app_views.route('/api/v1/stats')
def stats():
    """retrieves the number of each objects by type"""
    obj_count = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }

    return jsonify(obj_count), 200
