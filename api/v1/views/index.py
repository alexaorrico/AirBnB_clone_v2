#!/usr/bin/python3
"""
import app_views and create a route /status
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status")
def status_route():
    """returns a JSON: "status": "OK" """
    return jsonify({"status": "OK"})
