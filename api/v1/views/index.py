#!/usr/bin/python3
"""Create an index"""
from flask import jsonify
from api.v1.views import app_views
# app_views.url_map.strict_slashes = False


@app_views.route('/status', strict_slashes=False)
def status():
    """Return the status"""
    return jsonify({'status': 'OK'})
