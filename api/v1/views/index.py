#!/usr/bin/python3
"""
Status of touy API
"""

from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', strict_slashes=False)
def app_view():
    """
    object app_view
    """
    return jsonify({"status": "OK"})
