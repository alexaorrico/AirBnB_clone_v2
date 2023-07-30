#!/usr/bin/python3
"""
Craeted index view with /status route on object app_view
"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def get_status():
    """Gets the status of the API."""
    return jsonify("status"="OK")
