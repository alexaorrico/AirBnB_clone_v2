#!/usr/bin/python3
"""
Module for routing of index
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', methods=['GET'])
def status():
    """ Returns JSON with status "OK" """
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def stats():
    """ Returns retrieves the number of each objects by type """
    classes = {
        "Amenity": "amenities", "City": "cities",
        "Place": "places", "Review": "reviews",
        "State": "states", "User": "users"
    }
    new_dic = {}

    for cls_item, cls_name in classes.items():
        new_dic[cls_name] = storage.count(cls_item)

    return jsonify(new_dic)
