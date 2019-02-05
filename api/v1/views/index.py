#!/usr/bin/python3
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status", strict_slashes=False)
def status():
    """returns a JSON: "status": "OK"""
    return jsonify({"status": "OK"})


@app_views.route("/stats", strict_slashes=False)
def stats():
    """retrieves the number of each objects by type
    """
    cls_list = ["Amenity", "City", "Place",
                "Review", "State", "User"]
    cls_count = {}
    for cls in cls_list:
        cls_count[cls] = storage.count(cls)
    return jsonify(cls_count)
