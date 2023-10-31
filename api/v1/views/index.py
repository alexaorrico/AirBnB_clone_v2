#!/usr/bin/python3
"""
This is the endpoint (route) status
"""
from models import storage
from flask import Flask
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def get_status():
    """
    Route to return a JSON status
    """
    return jsonify({"status": "OK"})


@app_views.route('/api/v1/stats', methods=['GET'], strict_slashes=False)
def count():
    """
    Retrieves objects by their type
    """
    count = {}
    classes = ["User", "State", "City", "Amenity", "Place", "Review"]

    for cls in classes:
        count[cls] = storage.count(cls)

    return jsonify(count)
