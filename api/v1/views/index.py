#!/usr/bin/python3
"""Status of your API"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status")
def function():
    """function"""
    return jsonify({"status": "OK"})
