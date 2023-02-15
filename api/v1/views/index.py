#!/usr/bin/python3
"""
This module defines a Flask route /status and returns a JSON.
"""

from flask import jsonify
from api.v1.views import app_views


@app_views.route("/status", methods=["GET"])
def status():
    """
    Return a JSON with "status": "OK"
    """
    return jsonify({"status": "OK"})
