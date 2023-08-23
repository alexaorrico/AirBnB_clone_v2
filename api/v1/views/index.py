#!/usr/bin/python3
"""Index Module"""

from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def get_status():
    """Getting status of API """
    return jsonify(status="OK")
