#!/usr/bin/python3
from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status', strict_slashes=False)
def status():
    """ Returns the status of the http which should be 200 """
    return (jsonify({"status": "OK"}))


@app_views.route('/stats', strict_slashes=False)
def stats():
    i = 0
    ob_d = {"amenities": "Amenity", "cities": "City", "places": "Place",
            "reviews": "Review", "states": "State", "users": "User"}
    count_d = {}
    for k, v in ob_d.items():
        count_d[k] = storage.count(v)
    return(jsonify(count_d))
