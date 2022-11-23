#!/bin/usr/python3
"""Returns JSON status"""

from api.v1.views import app_views
from flask import jsonify

@app_views.route("/status")
def status():
    return jsonify({"status": "OK"})
