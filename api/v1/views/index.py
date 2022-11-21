#!/usr/bin/python3
"""
Module that creates /status route on app_views object
Returns "status": "OK" JSON
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status")
def status_route():
    """
    Returns "status": "OK" 
    """
    return jsonify({"status": "OK"})
