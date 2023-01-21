#!/usr/bin/python3
"""
Index view
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def status():
    """Return status of API"""
    return jsonify({'status': 'OK'})
