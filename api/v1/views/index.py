#!/usr/bin/python3
"""
index of API
"""

from api.v1.views import app_views
from flask import jsonify
from models import storage
dic_data = {
    "amenities": "Amenity",
    "cities": "City",
    "places": "Place",
    "reviews": "Review",
    "states": "State",
    "users": "User"
}



@app_views.route('/status', strict_slashes=False)
def hbnb_status():
    """ hbnb status """
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def app_status():
    """ app status"""

    for key, value in dic_data.items():
        dic_data[key] = storage.count(value)
    return jsonify(dic_data)