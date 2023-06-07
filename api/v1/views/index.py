#!/usr/bin/python3
"""Defines endpoints"""
from api.v1.views import app_views
from flask import jsonify

@app_views.route("/status")
def status():
    """Returns status of app"""
    return jsonify(status="OK")
