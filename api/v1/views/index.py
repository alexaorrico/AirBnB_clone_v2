#!/usr/bin/python3
"""
API index views module
"""
from api.v1.views import app_views
from models import storage
from flask import jsonify


@app_views.route('/status/')
def status():
    """
    Returns json response as the status 

    Returns:
        JSON: json object
    """
    status = {
        "status": "OK"
    }
    return jsonify(status)

@app_views.route('/stats/')
def count():
    """[summary]
    """

    models_avail = {
        "User": "users",
        "Amenity": "amenities", "city": "cities",
        "Place": "places", "Review": "reviews",
        "State": "states",
    }

    count = {}
    for cls in models_avail.keys():
        count[models_avail[cls]] = storage.count(cls)
    
    return jsonify(count)
