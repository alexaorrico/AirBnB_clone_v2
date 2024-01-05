#!/usr/bin/python3
"""
Flask API Route

This module defines a Flask route for the endpoint '/status'
The route returns a JSON response indicating the status as "OK"
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def display_status():
    """
    Route: /status

    Returns a JSON response indicating the status as "OK".

    Example:
    $ curl http://127.0.0.1:your_port/status
    Output: {"status": "OK"}
    """
    return jsonify(status="OK")
