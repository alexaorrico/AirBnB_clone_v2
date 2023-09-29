#!/usr/bin/python3
"""flask blueprint module"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status")
def status():
    """returns a json object of status"""
    return jsonify({"status": "OK"})
