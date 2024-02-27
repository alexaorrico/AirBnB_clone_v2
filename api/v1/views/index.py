#!/usr/bin/python3
"""
The file containing the index for the API
"""
from flask import jsonify

from api.v1.views import app_views
from models import storage


@app_views.route('/status')
def get_status():
    """Gets the status of the API.
    """
    return jsonify(status='OK')
