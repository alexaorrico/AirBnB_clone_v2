#!/usr/bin/python3
"""
api flask app
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status", strict_slashes=False)
def status():
    "function that show the status code"
    return jsonify(status="OK")
