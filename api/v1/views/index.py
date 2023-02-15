#!/usr/bin/python3
"""Views for the API status."""
from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status")
def status():
    """Return the API status."""
    return jsonify({"status": "OK"})
