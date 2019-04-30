#!/usr/bin/python3
"""Defines a status route for the HolbertonBnB API."""
from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status")
def server_status():
    """Returns the server status.

    Returns:
        JSON object with the current server status.
    """
    return jsonify({"status": "OK"})
