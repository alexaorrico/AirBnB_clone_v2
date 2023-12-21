#!/usr/bin/python3
"""
this module contains flask app routes
    flask APP routes:
        /status:    print jsonify "status"
"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status")
def status():
    "returns a serialized json data"
    return jsonify({"status": "OK"})
