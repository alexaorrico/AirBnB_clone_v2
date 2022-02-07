#!/usr/bin/python3
"""The home web Page"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status")
def status():
    """Return the a json dict status"""
    return jsonify({'status': 'OK'})
