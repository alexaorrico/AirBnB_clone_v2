#!/usr/bin/python3
"""index"""


from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def status():
    """return status"""
    stat = {"status": "OK"}
    json_response_stat = jsonify(stat)
    return json_response_stat


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

    json_obj_count = jsonify(obj_count)
    return (json_obj_count)
