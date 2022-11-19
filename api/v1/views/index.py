#!/usr/bin/python3
"""
Module implements a rule that returns the status of application
"""

from flask import jsonify
import models
from api.v1.views import app_views


@app_views.route('/status', strict_slashes=False)
def view_status():
    """
    Returns the status of API
    """
    return jsonify({"status": "OK"})
