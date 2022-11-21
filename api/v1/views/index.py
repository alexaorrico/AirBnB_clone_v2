#!/usr/bin/python3
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status", methods=['GET'])
def status():
    """ Status of API """
    return jsonify({"status": "OK"})


@app_views.route("/stats", methods=['GET'])
def stats():
    """ retrieves the number of each object by type"""
    obj = {}
    classes = ["amenities", "cities", "places", "reviews", "states", "users"]
    for cls in classes:
        obj[cls] = storage.count(cls)

    return jsonify(obj)
