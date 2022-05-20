#!/usr/bin/python3
"""
    link db to api
"""
from api.v1.views import app_views
from models import storage
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def status():
    """
        return satus of the api
    """
    return jsonify({"status": "OK"})

@app_views.route('/stats', strict_slashes=False)
def stats():
    """
        return number of objects
    """
    classes = {
        "Amenity": "amenities",
        "City": "cities",
        "Place": "places",
        "Review": "reviews",
        "State": "states",
        "User": "users"
    }
    
    response = {}
    for key, value in classes.items():
        response[value] = storage.count(key)
    return jsonify(response)
