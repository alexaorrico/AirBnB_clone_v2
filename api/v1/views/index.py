#!/usr/bin/python3
"""index conf"""
from api.v1.views import app_views
from flask import jsonify, request
from models import storage


@app_views.route('/status')
def status():
    """returns the status of the API: """
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def stats():
    """counts items of each class for all classes"""
    if request.method == 'GET':
        total_for_class = {}
        classes = {
                   "Amenity": "amenities",
                   "City": "cities",
                   "Place": "places",
                   "Review": "reviews",
                   "State": "states",
                   "User": "users"}
        for key, value in classes.items():
            total_for_class[value] = storage.count(key)
        return jsonify(total_for_class)
