#!/usr/bin/python3
"""Create a route that returns a JSON"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def status():
    """returns json file"""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def endpoint():
    """retrieves the number of each objects by type"""
    statss = {"Amenity": "amenities", "City": "cities", "Place": "places",
              "Review": "reviews", "State": "states", "User": "users"}
    stats_dic = {}
    for key, value in statss.items():
        stats_dic[value] = storage.count(key)
    return jsonify(stats_dic)
