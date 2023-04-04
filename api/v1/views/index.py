#!/usr/bin/python3
"""Route to index page"""
from json import dumps
from flask import jsonify
from api.v1.views import app_views

cc = {"Amenity": "amenities", "City": "cities", "Place": "places",
      "Review": "reviews", "State": "states", "User": "users"}


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Return status of API"""
    return jsonify(dumps({"status": "OK"}), content_type='application/json')


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """Return number of objects by type"""
    data = {}
    for cls in cc.keys():
        data[cc[cls]] = cc.count(cls)
    return jsonify(dumps(data), content_type='application/json')
