#!/usr/bin/python3
"""
This module defines the status route for the API.
"""


from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'])
def get_status():
    """
    Returns the status of the API.
    """
    return jsonify({"status": "OK"})
