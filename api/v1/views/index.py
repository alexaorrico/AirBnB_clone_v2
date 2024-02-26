#!/usr/bin/python3
"""Status route for the AirBnB API"""
from flask import jsonify
from api.v1.views import app_views


@app_views.route("/status")
def status():
    """Returns the status of the server"""
    return jsonify({"status": "OK"})
