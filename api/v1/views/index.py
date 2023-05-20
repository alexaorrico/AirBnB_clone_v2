#!/usr/bin/python3
"""index page"""
from flask import jsonify
from api.v1.views import app_views


@app_views.route("/status")
def status():
    """Returns OK"""
    return jsonify({"status": "OK"})
