#!/usr/bin/python3
"""Creation of API endpoints"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def status_api():
    """Returning API status"""
    return (jsonify({"status": "OK"}))
