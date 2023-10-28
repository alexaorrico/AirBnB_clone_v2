#!/usr/bin/python3
"""
views for our project
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def ok_status():
    """
    return an ok json status
    """
    return jsonify({"status": "OK"})

@app_views.route('/stats/')
def stats():
    """
    endpoint returns stats
    returns a number of objects of each class
    """
    models = {"User": "users",
              "Amenity": "amenities", "City": "cities",
              "Place": "places", "Review": "reviews",
              "State": "states"}
    stats = {}
    for cls in models.keys():
        stats[models[cls]] = storage.count(cls)
    return jsonify(stats)
