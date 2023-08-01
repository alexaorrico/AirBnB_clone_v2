#!/usr/bin/python3
"""create a route /status on the object app_views
that returns a JSON"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status")
def status():
    """returns a JSON with status OK"""
    if request.method == 'GET':
        return jsonify({'status': 'OK'})


@app_views.route("/stats")
def stats():
    '''
        return counts of all classes in storage
    '''
    if request.method == 'GET':
        response = {}
    obj_counts = {
            "Amenity": "amenities",
            "City": "cities",
            "Place": "places",
            "Review": "reviews",
            "State": "states",
            "User": "users"
            }
    for key, value in obj_counts.items():
        response[value] = storage.count(key)
    return jsonify(response)
