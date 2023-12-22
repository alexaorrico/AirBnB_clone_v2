#!/usr/bin/python3
"""Index routes for API"""

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', methods=['GET'])
def status():
    """Returns the status of the API"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def stats():
    """Returns the count of various objects by type"""
    classes = {
        "Amenity": "amenities",
        "City": "cities",
        "Place": "places",
        "Review": "reviews",
        "State": "states",
        "User": "users"
    }
    counts = {cls_name: storage.count(cls_obj) for cls_obj,
              cls_name in classes.items()}
    return jsonify(counts)
