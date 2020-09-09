#!/usr/bin/python3
"""This module is in charge of managing the index."""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status():
    """Return the current status.

    Returns:
        dict: "OK"

    """
    return jsonify({"status": "OK"})
