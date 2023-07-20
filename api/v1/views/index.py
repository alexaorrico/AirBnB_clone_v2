#!/usr/bin/python3
"""Module for index endpoint of the views module of v1 of the RESTful API"""

from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status', methods=['GET'])
def status():
    """Returns the status of the API."""
    return jsonify({"status": "OK"})
