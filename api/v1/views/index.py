#!/usr/bin/python3
"""
This module defines a route status for a Flask application.

The route /status is defined on the Flask application instance app_views.
When a GET request is sent to /status, the status function is executed.
"""

from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'])
def status():
    """
    Return the server status as JSON.

    When this function is called, it returns a JSON response with a single
    key-value pair. The key is "status" and the value is "OK".
    """
    return jsonify({"status": "OK"})
