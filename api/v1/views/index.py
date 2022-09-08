#!/usr/bin/python3
"""
Status of your API
"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status():
    message = {"status": "OK"}
    return jsonify(message)
