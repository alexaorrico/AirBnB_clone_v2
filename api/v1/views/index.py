#!/usr/bin/python3
"""Flask app"""
from flask import Flask, Blueprint, jsonify, request
from api.v1.views import app_views
from models import storage


@app_views.route('/status', methods=['GET'])
def status():
    if request.method == 'GET':
        return jsonify({"status": "OK"})


@app_views.route('/stats')
def count():
    """
        counts object
    """

    dictionary = {}
    clss = {
        "Amenity": "amenities",
        "Place": "places",
        "State": "states",
        "City": "cities",
        "Review": "reviews",
        "User": "users"
    }

    for cls in clss:
        count = storage.count(cls)
        dictionary[clss.get(cls)] = count
    return jsonify(dictionary)
