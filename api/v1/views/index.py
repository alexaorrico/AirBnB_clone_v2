#!/usr/bin/python3
""" API Endpoint """
from flask import jsonify
from api.v1.views import app_views

classes = {"amenities": "Amenity",
           "cities": "City",
           "places": "Place",
           "reviews": "Review",
           "states": "State",
           "users": "User"}


@app_views.route('/status', strict_slashes=False)
def test():
    """check status of the api"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def counts():
    """endpoint that retrieves the number of each objects by typ"""
    from models import storage
    count_dict = {}
    for k, v in classes.items():
        count_dict[k] = storage.count(v)
    return jsonify(count_dict)
