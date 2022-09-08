#!/usr/bin/python3
"""index"""
from api.v1.views import app_views
from flask import jsonify, request
from models import storage


@app_views.route('/status')
def status():
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def stats():
    dic = {}
    classes = {"amenities": "Amenity", "cities": "City",
               "places": "Place", "reviews": "Review",
               "states": "State", "users": "User"}
    for key, value in classes.items():
        dic[key] = storage.count(value)
    return dic
