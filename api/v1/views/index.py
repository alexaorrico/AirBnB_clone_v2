#!/usr/bin/python3
""" Index module"""
from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage


@app_views.route('/status', strict_slashes=False)
def status_jsn():
    """return a json status"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def stats_jsn():
    """return json stats representation"""
    options = {
        "Amenity": "amenities",
        "City": "cities",
        "Place": "places",
        "Review": "reviews",
        "State": "states",
        "User": "users"
        }
    opt_dic = {}
    for k, v in options.items():
        opt_dic[v] = storage.count(k)
    return jsonify(opt_dic)
