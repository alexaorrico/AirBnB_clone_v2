#!/usr/bin/python3
"""
creates the route
"""
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'])
def status():
    """
    Gets the status of the API and returns it
    """
    return jsonify(status="OK")
