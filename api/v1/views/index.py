#!/usr/bin/python3
"""Views index module"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', strict_slashes=False)
def status_route():
    """status route function: return OK"""
    return jsonify({'status': 'OK'})


@app_views.route('/stats', strict_slashes=False)
def hbnbStats():
    """stats route function"""
    res_model = {
        "amenities": "Amenity",
        "cities": "City",
        "places": "Place",
        "reviews": "Review",
        "states": "State",
        "users": "User"
    }
    res = {}
    for key, value in res_model.items():
        res[key] = storage.count(value)
    return jsonify(res)
