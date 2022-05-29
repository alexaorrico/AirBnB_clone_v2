#!/usr/bin/python3
"""
create a route /status on the object app_views that returns a JSON
"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status", strict_slashes=False)
def status_route():
    """
    returns a JSON: "status": "OK"
    """
    return jsonify({"status": "OK"})
