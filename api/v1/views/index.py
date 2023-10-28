#!/usr/bin/python3
"""
This module imports the app view blueprint and defines
all associated methods with the blueprint
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status")
def api_ok():
    """
    This function simply determines if server
    serving api's is up and running
    """
    return jsonify({"status": "OK"})
