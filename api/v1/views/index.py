#!/usr/bin/python3
"""run script"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status")
def status():
    """returns a json representation of status"""
    return jsonify({"status": "OK"})
