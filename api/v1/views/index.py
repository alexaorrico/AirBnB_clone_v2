#!/usr/bin/python3
"""
App views for AirBnB_clone_v3
"""

from api.v1.views import app_views
from flask import jsonify, request
from models import storage
from models import *


@app_views.route('/status', methods=['GET'])
def status():
    """ returns status """
    status = {"status": "OK"}
    return jsonify(status)


@app_views.route('/stats', methods=['GET'])
def stats():
    """
    function to return the count of all class objects
    """
    total = {}
    classes = {"Amenity": "amenities",
               "City": "cities",
               "Place": "places",
               "Review": "reviews",
               "State": "states",
               "User": "users"}
    for cls in classes:
        count = storage.count(cls)
        total[classes.get(cls)] = count
    return jsonify(total)
