#!/usr/bin/python3
"""
index.py
This module creates a route /status on the object app_views
that returns a JSON: "status": "OK"
"""

from flask import jsonify
from api.v1.views import app_views


@app_views.route("/status", methods=["GET"])
def show_status():
    """ returns a JSON that displays the status """
    return jsonify({"status": "OK"})
