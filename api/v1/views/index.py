#!/usr/bin/python3
"""
index of API
"""

from api.v1.views import app_views
from flask import jsonify, make_response
from models import storage
dic_data = {
    "amenities": "Amenity",
    "cities": "City",
    "places": "Place",
    "reviews": "Review",
    "states": "State",
    "users": "User"
}


@app_views.route('/status', methods=['GET'],  strict_slashes=False)
def status():
    """ Status of API """
    return make_response(jsonify({"status": "OK"}))


@app_views.route('/stats',methdos=['GET'], strict_slashes=False)
def app_status():
    """ app status"""
    for key, value in dic_data.items():
        dic_data[key] = storage.count(value)
    return jsonify(dic_data)
