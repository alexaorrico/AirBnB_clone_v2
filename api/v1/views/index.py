#!/usr/bin/python3
"""This is the index module"""

from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route("/status", methods=["GET"])
def status():
    """Returns a JSON response with status: OK"""
    return jsonify(status="OK")


@app_views.route("/api/v1/stats", methods=["GET"])
def get_stats():
    """
    Retrieves the number of each object type.

    Returns:
        A JSON response with the count of each object type.
    """
    stats = {}
    for cls in storage.classes.values():
        cls_name = cls.__name__
        count = storage.count(cls)
        stats[cls_name] = count

    return jsonify(stats)
