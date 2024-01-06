#!/usr/bin/python3
"""flask with general route"""

from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'])
def apiStatus():
    """return JSON OK status"""
    return jsonify({"status": "OK"})
