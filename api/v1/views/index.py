#!/usr/bin/python3

from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status', strict_slashes=False)
def status():
    """shows the status of a request"""
    status = {"status": "OK"}
    return jsonify(status)
