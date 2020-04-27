#!/usr/bin/python3
"""
Flask index file that returns the json status response
"""
from api.v1.views import app_views
from models import storage
from flask import jsonify
from flask import request


@app_views.route('/status', methods=['GET'])
def status():
    """
    function for status route that returns the status
    """
    if request.method == 'GET':
        resp = {"status": "OK"}
        return jsonify(resp)


@app_views.route("/stats", methods=['GET'])
def count_objects():
    """
    function for count each obj in each class
    """
    list_class = ["Amenity", "City", "Place", "Review", "State", "User"]
    dict_class = {}
    for item in list_class:
        dict_class[item] = storage.count(item)
    return jsonify(dict_class)
