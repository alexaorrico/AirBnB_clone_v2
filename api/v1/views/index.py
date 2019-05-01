#!/usr/bin/python3
"""Routing for AirBnB"""
from api.v1.views import app_views
from flask import jsonify, request
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Gets the status of the application"""
    if request.method == 'GET':
        return jsonify({'status': 'OK'})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """Gives object count of each class"""
    dic = {}
    classes = [
        "Amenity",
        "City",
        "Place",
        "Review",
        "State",
        "User"
    ]
    class_plural = [
        "amenities",
        "cities",
        "places",
        "reviews",
        "states",
        "users"
    ]

    j = 0
    for i in classes:
        count = storage.count(i)
        dic[class_plural[j]] = count
        j += 1

    if request.method == 'GET':
        return jsonify(dic)
