#!/usr/bin/python3
"""
This module defines a Flask blueprint for handling status requests.
"""

from api.v1.views import app_views
from flask import jsonify

@app_views.route("/status", methods=["GET"], strict_slashes=False)
def api_status():
    """a function to return api status"""
    data = {
        "status": "OK"
    }

    shojo = jsonify(data)
    shojo.status_code = 200
    return shojo