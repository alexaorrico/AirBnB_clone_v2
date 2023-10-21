#!/usr/bin/python3
"""
Index module
"""
from flask import jsonify
from views import app_views
from models import storage


@app_views.route('/api/v1/stats', methods=['GET'])
def status():
    """
    Returns status: OK in JSON format
    """
    stats = {}
    classes = ["Amenity", "City", "Place", "Review", "State", "User"]
    for class_name in classes:
        count = storage.count(class_name)
        stats[class_name] = count
    return jsonify(stats)
