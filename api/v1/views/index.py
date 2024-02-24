#!/usr/bin/python3
"""
Index file
"""
from api.v1.views import app_views
from flask import jsonify, make_response
from models import storage


@app_views.route('/status')
def status():
    """Gives status 200 message"""
    return make_response(jsonify({"status": "OK"}), 200)


@app_views.route('/stats')
def obj_types():
    """retrieves the number of each objects by type"""
    type_data = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }

    resp = jsonify(type_data)
    resp.status_code = 200

    return resp
