#!/usr/bin/python3
""" Index module """
from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """returns a json"""
    return jsonify({"status": "OK"})
    
@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """retrieves the number of each objects by type"""
    v_class = {
            "amenities": "Amenity",
            "cities": "City",
            "places": "Place",
            "reviews": "Review",
            "states": "State",
            "users": "User"
            }

    obj = {}

    for key, value in v_class.items():
        count = storage.count(value)
        obj[key] = count
    return jsonify(obj)

