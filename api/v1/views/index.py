#!/usr/bin/python3
"""
Module for status and stats endpoint
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status", methods=['GET'], strict_slashes=False)
def status():
    """
    create a route /status on the object app_views
    that returns a JSON: "status": "OK"
    """
    return jsonify({'status': 'OK'})
