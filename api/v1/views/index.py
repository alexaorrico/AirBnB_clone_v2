#!/usr/bin/python3
"""
index module
"""

from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage


@app_views.route("/status", methods=["GET"])
def status():
    """
    returns json string
    """
    return jsonify({"status": "OK"})

@app_views.route("/stats", methods=["GET"])
def stats_class_count():
    """Retrieves the number of each object by type"""
    dic = {
            'amenities': storage.count('Amenity'),
            'cities': storage.count('City'),
            'places': storage.count('Place'),
            'reviews': storage.count('Review'),
            'states': storage.count('State'),
            'users': storage.count('User')
          }
    return jsonify(dic)
