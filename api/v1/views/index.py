#!/usr/bin/python3
"""Index Module"""

from api.v1.views import app_views


@app_views.route('/status')
def status():
    """Return status OK"""
    return jsonify({"status": "OK"}), 200
