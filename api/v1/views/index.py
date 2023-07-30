#!/usr/bin/python3
"""Status module
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def status():
    """Returns JSON status OK
    """
    return jsonify(status="OK")
