#!/usr/bin/python3
"""API Routes"""
from flask import jsonify

from api.v1.views import app_views


@app_views.route('/status')
def api_status():
    """return the API status"""
    return jsonify({"status": "OK"})
