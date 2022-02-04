#!/usr/bin/python3
"""
Script that starts a Flask web application
"""
from api.v1.views import app_views

from models import storage
from flask import jsonify


classes = {"Amenity": "amenities",
           "City": "cities",
           "Place": "places",
           "Review": "reviews",
           "State": "states",
           "User": "users"}


@app_views.route('/status')
def status():
    """ Returns a JSON: "status": "OK"""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def count_stats():
    """ Create an endpoint that retrieves the number of each objects by type"""
    count_dic = {}
    for v, k in classes.items():
        count_dic[k] = storage.count(v)

    return jsonify(count_dic)
