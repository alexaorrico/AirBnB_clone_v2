#!/usr/bin/python3
"""
Flask route that returns json status response
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status/")
def status():
    """
    function for status route that returns the status
    """
    return jsonify({"status": "OK"})
