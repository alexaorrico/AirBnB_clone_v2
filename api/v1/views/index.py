#!/usr/bin/python3

"""
Creating a blueprint with the URL prefix
"""

from flask import Blueprint, jsonify


# Create a blueprint with the URL
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')


# Define route
@app_views.route('/status', methods=['GET'])
def get_status():
    """Returns a JSON response indicating the status is OK."""
    return jsonify({"status": "OK"})
