#!/usr/bin/python3
"""creating route on app_views obj"""

from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status')
def status():
    """returns a JSON and The Status"""
    return jsonify({"status": "OK"})
