#!/usr/bin/python3
"""index page"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status")
def message():
    """return: status ok"""
    return jsonify({"status": "OK"})
