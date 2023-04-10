#!/usr/bin/python3
"""
import app_views from api.v1.views
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', methods=['GET'])
def status():
    """
    Returns the status of the application
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def stats():
    """
    Returns the number of objects by type
    """
    counts = {}
    classes = ['Amenity', 'City', 'Place', 'Review', 'State', 'User']
    for cls in classes:
        counts[cls] = storage.count(cls)
    return jsonify(counts)
