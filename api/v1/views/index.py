#!/usr/bin/python3
"""
module creates a route /status on any object app_views
return: JSON: "status: OK"
"""
from api.v1.views import app_views
from flask import jsonify

@app_views.route("/status")
def status():
    """
    Returns OK if JSON works
    """
    j_status = {"status": "OK"}
    return jsonify(j_status)
