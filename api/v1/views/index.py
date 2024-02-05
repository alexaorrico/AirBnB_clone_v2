#!/usr/bin/python3
"""a module as an index"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status", strict_slashes=False)
def status():
    """a function to return status OK when visit /status"""
    return jsonify({"status": "OK"})
