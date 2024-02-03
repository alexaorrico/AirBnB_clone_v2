#!/usr/bin/python3
"""
Index for our web flask
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Return status OK"""
    return jsonify(status="OK")

@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """Retrieve the number of each objects by type"""
    classes = {"Amenity": "amenities", "City": "cities",
               "Place": "places", "Review": "reviews",
               "State": "states", "User": "users"}
    counts = {}
    for class_name in classes:
        counts[classes[class_name]] = storage.count(class_name)
    return jsonify(counts)
