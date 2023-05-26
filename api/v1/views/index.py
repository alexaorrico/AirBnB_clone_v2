#!/usr/bin/python3
"""
Module contains status endpoint
"""

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status")
def get_status():
    """
    Endpoint to get API status
    """
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def storage_counts():
    '''
    return all the counts of all the classes contain in storage
    '''
    cls_counts = {
            "amenities": storage.count("Amenity"),
            "cities": storage.count("City"),
            "place": storage.count("Place"),
            "reviews": storage.count("Review"),
            "states": storage.count("State"),
            "users": storage.count("Users")
    }
    return jsonify(cls_counts)
