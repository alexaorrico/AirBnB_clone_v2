#!/usr/bin/python3
"""
module with route /status on object app_views
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage

class_dict = {
    "amenities": "Amenity",
    "cities": "City",
    "places": "Place",
    "reviews": "Review",
    "states": "State",
    "users": "User",
}


@app_views.route('/status')
def status():
    """
    returns an OK Jsonified
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def storage_count():
    """
    retrieves the number of each objects per type
    """
    cls_count = {}
    for k in class_dict:
        cls_count[k] = storage.count(class_dict[k])
    return jsonify(cls_count)
