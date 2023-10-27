#!/usr/bin/python3
"""for the following files"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status")
def status():
    """return the status of the application"""
    return jsonify({"status": "OK"})
