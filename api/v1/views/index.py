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
    classes = [
        "Amenity", "BaseModel", "City",
        "Place", "Review", "State", "User"
        ]
    new_dic = {}

    for cls_item in classes:
        new_dic[cls_item] = storage.count(cls_item)

    return jsonify(new_dic)
